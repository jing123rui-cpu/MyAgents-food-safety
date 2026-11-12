# -*- coding: utf-8 -*-
"""本地语义检索（RAG）——嵌入 + SQLite 向量索引。

设计取舍：
- 只依赖 numpy（已随环境安装），不引入 chromadb/faiss，避免 Python 3.14 的轮子兼容问题；
- 向量存 SQLite BLOB，检索时读入内存做点积（语料约 1000 chunk，内存占用几 MB）；
- 嵌入走 paratera 的 GLM-Embedding-2（OpenAI 兼容 /v1/embeddings）。

密钥解析顺序（不写入仓库）：
1. 环境变量 PARATERA_API_KEY
2. ~/.local/share/opencode/auth.json 中 provider 的 key
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

# ── 配置 ──────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parents[2]          # audit/script/rag.py -> repo root
DB_PATH = ROOT / "audit" / ".index" / "rag.db"

EMBED_URL = os.environ.get("PARATERA_EMBEDDING_URL", "https://llmapi.paratera.com/v1/embeddings")
EMBED_MODEL = os.environ.get("PARATERA_EMBEDDING_MODEL", "GLM-Embedding-2")
PROVIDER_ID = os.environ.get("PARATERA_PROVIDER_ID", "myprovider1109-")

CHUNK_TARGET = 800
CHUNK_OVERLAP = 120
MIN_CHUNK = 40
BATCH_SIZE = 16
CHUNK_VERSION = "2"
EMBED_WORKERS = max(1, int(os.environ.get("PARATERA_EMBEDDING_WORKERS", "3")))

# (显示名, 目录/文件, 扩展名)
SOURCES: dict[str, tuple[Path, tuple[str, ...]]] = {
    "knowledge": (ROOT / "audit" / "knowledge", (".md", ".yaml", ".yml")),
    "skills": (ROOT / "skills" / "food-safety-audit", (".md",)),
}
EXTRA_FILES = [ROOT / "AGENTS.md", ROOT / "README.md"]
SKIP_NAMES = {"knowledge-index.md"}


# ── 嵌入 ──────────────────────────────────────────────────────────

class EmbeddingError(RuntimeError):
    pass


def resolve_api_key() -> str:
    key = os.environ.get("PARATERA_API_KEY", "").strip()
    if key:
        return key

    auth_path = Path.home() / ".local" / "share" / "opencode" / "auth.json"
    if auth_path.is_file():
        try:
            data = json.loads(auth_path.read_text(encoding="utf-8"))
            entry = data.get(PROVIDER_ID) or {}
            key = str(entry.get("key") or "").strip()
            if key:
                return key
        except (OSError, ValueError) as exc:
            raise EmbeddingError(f"读取 {auth_path} 失败：{exc}") from exc

    raise EmbeddingError(
        "找不到嵌入模型密钥。请设置环境变量 PARATERA_API_KEY，"
        f"或在 {auth_path} 中配置 provider {PROVIDER_ID}。"
    )


def _embed_batch(batch: list[str], key: str, timeout: int) -> list[list[float]]:
    payload = json.dumps({"model": EMBED_MODEL, "input": batch}).encode("utf-8")
    last_err: Exception | None = None

    for attempt in range(4):
        req = urllib.request.Request(
            EMBED_URL,
            data=payload,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.load(resp)
            items = sorted(data.get("data", []), key=lambda x: x.get("index", 0))
            vectors = [item["embedding"] for item in items]
            if len(vectors) != len(batch):
                raise EmbeddingError(f"返回条数不符：请求 {len(batch)}，返回 {len(vectors)}")
            return vectors
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
            last_err = EmbeddingError(f"HTTP {exc.code}: {detail}")
            if exc.code in (400, 401, 403, 404):
                break
        except Exception as exc:  # noqa: BLE001 - 网络错误统一重试
            last_err = exc
        time.sleep(1.5 ** attempt)

    raise EmbeddingError(f"嵌入请求失败：{last_err}")


def embed_texts(texts: Sequence[str], *, timeout: int = 90) -> np.ndarray:
    """返回 L2 归一化的 float32 矩阵 (n, dim)。"""
    if not texts:
        return np.zeros((0, 0), dtype=np.float32)

    key = resolve_api_key()
    batches = [list(texts[i:i + BATCH_SIZE]) for i in range(0, len(texts), BATCH_SIZE)]
    results: list[list[list[float]] | None] = [None] * len(batches)

    with ThreadPoolExecutor(max_workers=EMBED_WORKERS) as pool:
        futures = {
            pool.submit(_embed_batch, batch, key, timeout): idx
            for idx, batch in enumerate(batches)
        }
        for future in as_completed(futures):
            results[futures[future]] = future.result()

    out = [vec for batch in results if batch for vec in batch]
    arr = np.asarray(out, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return arr / norms


# ── 切块 ──────────────────────────────────────────────────────────

@dataclass
class Chunk:
    heading: str
    text: str


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _window(lines: list[str], target: int, overlap: int) -> list[str]:
    """按行窗口切分，尽量不截断段落。"""
    text = "\n".join(lines).strip()
    if len(text) <= target:
        return [text] if text else []

    out: list[str] = []
    buf: list[str] = []
    size = 0
    for line in lines:
        if size + len(line) + 1 > target and buf:
            out.append("\n".join(buf).strip())
            tail: list[str] = []
            tail_size = 0
            for prev in reversed(buf):
                if tail_size + len(prev) + 1 > overlap:
                    break
                tail.insert(0, prev)
                tail_size += len(prev) + 1
            buf, size = tail, tail_size
        buf.append(line)
        size += len(line) + 1
    if buf:
        out.append("\n".join(buf).strip())
    return [c for c in out if c]


def split_markdown(text: str) -> list[Chunk]:
    sections: list[tuple[str, list[str]]] = []
    stack: list[tuple[int, str]] = []
    buf: list[str] = []
    in_fence = False

    def flush() -> None:
        body = "\n".join(buf).strip()
        if body:
            sections.append((" / ".join(t for _, t in stack), buf[:]))
        buf.clear()

    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        match = _HEADING_RE.match(line) if not in_fence else None
        if match:
            flush()
            level = len(match.group(1))
            stack = [item for item in stack if item[0] < level]
            stack.append((level, match.group(2).strip()))
        else:
            buf.append(line)
    flush()

    chunks: list[Chunk] = []
    for heading, lines in sections:
        for part in _window(lines, CHUNK_TARGET, CHUNK_OVERLAP):
            if len(part) >= MIN_CHUNK or len(sections) == 1:
                chunks.append(Chunk(heading=heading or "（无标题）", text=part))
    return chunks


def split_yaml(text: str) -> list[Chunk]:
    lines = text.splitlines()
    blocks: list[tuple[str, list[str]]] = []
    current: list[str] = []
    heading = ""

    for line in lines:
        if re.match(r"^- id:\s*", line) and current:
            blocks.append((heading, current))
            current, heading = [line], line.strip()
        else:
            if line.startswith("#") and not heading and not current:
                heading = line.lstrip("# ").strip()
            current.append(line)
    if current:
        blocks.append((heading, current))

    if not blocks:
        blocks = [("", lines)]

    chunks: list[Chunk] = []
    for head, block in blocks:
        for part in _window(block, CHUNK_TARGET, CHUNK_OVERLAP):
            if len(part) >= MIN_CHUNK:
                chunks.append(Chunk(heading=head or "（无标题）", text=part))
    if chunks and all(c.heading == "（无标题）" for c in chunks):
        id_match = re.search(r"^id:\s*(\S+)", text, re.MULTILINE)
        title_match = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
        label = " · ".join(
            x for x in [
                id_match.group(1) if id_match else "",
                title_match.group(1).strip() if title_match else "",
            ] if x
        )
        if label:
            for chunk in chunks:
                chunk.heading = label
    return chunks


def split_file(path: Path) -> list[Chunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    if path.suffix.lower() in (".yaml", ".yml"):
        return split_yaml(text)
    return split_markdown(text)


# ── 索引 ──────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
CREATE TABLE IF NOT EXISTS files (
    path TEXT PRIMARY KEY,
    mtime REAL NOT NULL,
    size INTEGER NOT NULL,
    sha TEXT NOT NULL,
    n_chunks INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL,
    heading TEXT NOT NULL,
    ordinal INTEGER NOT NULL,
    text TEXT NOT NULL,
    dim INTEGER NOT NULL,
    vector BLOB NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chunks_path ON chunks(path);
"""


@dataclass
class IndexStats:
    files_total: int = 0
    files_embedded: int = 0
    files_skipped: int = 0
    files_removed: int = 0
    chunks: int = 0
    seconds: float = 0.0


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _iter_files(scopes: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for scope in scopes:
        if scope == "repo":
            files.extend(p for p in EXTRA_FILES if p.is_file())
            continue
        if scope not in SOURCES:
            raise ValueError(f"未知 scope：{scope}（可选 {', '.join(SOURCES)}）")
        base, exts = SOURCES[scope]
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if (
                path.is_file()
                and path.suffix.lower() in exts
                and path.name not in SKIP_NAMES
                and "__pycache__" not in path.parts
            ):
                files.append(path)
    return sorted(set(files))


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_index(scopes: Sequence[str] = ("knowledge", "skills"), *, force: bool = False) -> IndexStats:
    started = time.time()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)

    dim_row = con.execute("SELECT value FROM meta WHERE key = 'dim'").fetchone()
    embed_dim = int(dim_row[0]) if dim_row else 0
    model_row = con.execute("SELECT value FROM meta WHERE key = 'model'").fetchone()
    stored_model = model_row[0] if model_row else None
    chunk_row = con.execute("SELECT value FROM meta WHERE key = 'chunk_version'").fetchone()
    stored_chunk = chunk_row[0] if chunk_row else None
    if force or (stored_model and stored_model != EMBED_MODEL) or stored_chunk != CHUNK_VERSION:
        con.execute("DELETE FROM chunks")
        con.execute("DELETE FROM files")

    known = {row[0]: row[1:] for row in con.execute("SELECT path, mtime, size, sha FROM files")}
    files = _iter_files(scopes)
    stats = IndexStats(files_total=len(files))

    pending: list[tuple[Path, str, float, int, str, list[Chunk]]] = []
    seen: set[str] = set()

    for path in files:
        rel = _rel(path)
        seen.add(rel)
        stat = path.stat()
        if not force and rel in known:
            mtime, size, sha = known[rel]
            if abs(mtime - stat.st_mtime) < 1e-6 and size == stat.st_size:
                stats.files_skipped += 1
                continue
            if _sha256(path) == sha:
                con.execute("UPDATE files SET mtime = ?, size = ? WHERE path = ?", (stat.st_mtime, stat.st_size, rel))
                stats.files_skipped += 1
                continue
        pending.append((path, rel, stat.st_mtime, stat.st_size, _sha256(path), split_file(path)))

    removed = [p for p in known if p not in seen]
    for rel in removed:
        con.execute("DELETE FROM chunks WHERE path = ?", (rel,))
        con.execute("DELETE FROM files WHERE path = ?", (rel,))
    stats.files_removed = len(removed)

    # 空文件先落库，其余汇总后统一嵌入（跨文件批处理更快）
    embeddable: list[tuple[Path, str, float, int, str, list[Chunk]]] = []
    for item in pending:
        path, rel, mtime, size, sha, chunks = item
        if chunks:
            embeddable.append(item)
            continue
        con.execute("DELETE FROM chunks WHERE path = ?", (rel,))
        con.execute(
            "INSERT INTO files(path, mtime, size, sha, n_chunks) VALUES (?, ?, ?, ?, 0) "
            "ON CONFLICT(path) DO UPDATE SET mtime=excluded.mtime, size=excluded.size, sha=excluded.sha, n_chunks=0",
            (rel, mtime, size, sha),
        )

    flat_inputs: list[str] = []
    for _, _, _, _, _, chunks in embeddable:
        flat_inputs.extend(
            f"{chunk.heading}\n{chunk.text}" if chunk.heading else chunk.text
            for chunk in chunks
        )

    vectors = embed_texts(flat_inputs) if flat_inputs else np.zeros((0, 0), dtype=np.float32)
    offset = 0
    for path, rel, mtime, size, sha, chunks in embeddable:
        file_vectors = vectors[offset:offset + len(chunks)]
        offset += len(chunks)
        embed_dim = int(file_vectors.shape[1]) if file_vectors.size else embed_dim

        con.execute("DELETE FROM chunks WHERE path = ?", (rel,))
        con.executemany(
            "INSERT INTO chunks(path, heading, ordinal, text, dim, vector) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (rel, chunk.heading, i, chunk.text, int(vec.shape[0]), vec.astype(np.float32).tobytes())
                for i, (chunk, vec) in enumerate(zip(chunks, file_vectors))
            ],
        )
        con.execute(
            "INSERT INTO files(path, mtime, size, sha, n_chunks) VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(path) DO UPDATE SET mtime=excluded.mtime, size=excluded.size, sha=excluded.sha, n_chunks=excluded.n_chunks",
            (rel, mtime, size, sha, len(chunks)),
        )
        con.commit()
        stats.files_embedded += 1
        stats.chunks += len(chunks)
        print(f"  + {rel}  ({len(chunks)} chunks)", flush=True)

    stats.chunks = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    con.execute("INSERT INTO meta(key, value) VALUES ('model', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (EMBED_MODEL,))
    con.execute("INSERT INTO meta(key, value) VALUES ('dim', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(embed_dim),))
    con.execute("INSERT INTO meta(key, value) VALUES ('chunk_version', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (CHUNK_VERSION,))
    con.execute("INSERT INTO meta(key, value) VALUES ('updated_at', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (time.strftime("%Y-%m-%dT%H:%M:%S"),))
    con.commit()
    con.close()
    stats.seconds = time.time() - started
    return stats


# ── 检索 ──────────────────────────────────────────────────────────

@dataclass
class Hit:
    score: float
    path: str
    heading: str
    text: str


SCOPE_PREFIX = {
    "knowledge": "audit/knowledge/",
    "skills": "skills/",
}

_ASCII_RE = re.compile(r"[a-z0-9]+")
_CJK_RE = re.compile(r"[\u4e00-\u9fff]+")
_STOP = {"the", "and", "for", "with", "from", "that", "this", "are", "was", "not"}


def _tokens(text: str) -> set[str]:
    low = text.lower()
    tokens = {w for w in _ASCII_RE.findall(low) if len(w) > 1 and w not in _STOP}
    for run in _CJK_RE.findall(low):
        if len(run) == 1:
            tokens.add(run)
        else:
            tokens.update(run[i:i + 2] for i in range(len(run) - 1))
    return tokens


def _keyword_score(query_tokens: set[str], text: str) -> float:
    if not query_tokens:
        return 0.0
    matched = query_tokens & _tokens(text)
    if not matched:
        return 0.0
    return sum(len(t) for t in matched) / sum(len(t) for t in query_tokens)


def search_index(query: str, *, k: int = 5, scope: str = "all") -> list[Hit]:
    if not DB_PATH.is_file():
        raise FileNotFoundError(f"索引不存在：{DB_PATH}。先运行 index。")

    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    sql = "SELECT path, heading, text, dim, vector FROM chunks"
    params: tuple = ()
    if scope != "all":
        prefix = SCOPE_PREFIX.get(scope)
        if not prefix:
            raise ValueError(f"未知 scope：{scope}（可选 all, knowledge, skills）")
        sql += " WHERE path LIKE ?"
        params = (prefix + "%",)
    rows = con.execute(sql, params).fetchall()
    con.close()
    if not rows:
        return []

    qvec = embed_texts([query])[0]
    dim = rows[0][3]
    if qvec.shape[0] != dim:
        raise RuntimeError(f"维度不匹配：查询 {qvec.shape[0]}，索引 {dim}。重建索引。")

    mat = np.vstack([np.frombuffer(row[4], dtype=np.float32) for row in rows])
    cosine = mat @ qvec

    query_tokens = _tokens(query)
    hybrid = np.array(
        [
            0.65 * float(cosine[i]) + 0.35 * _keyword_score(query_tokens, f"{rows[i][1]}\n{rows[i][2]}")
            for i, row in enumerate(rows)
        ],
        dtype=np.float32,
    )

    # 同一文件最多 2 条，避免一份文档占满结果
    order = np.argsort(-hybrid)
    hits: list[Hit] = []
    per_path: dict[str, int] = {}
    for i in order:
        path = rows[i][0]
        if per_path.get(path, 0) >= 2:
            continue
        per_path[path] = per_path.get(path, 0) + 1
        hits.append(Hit(float(hybrid[i]), path, rows[i][1], rows[i][2]))
        if len(hits) == k:
            break
    return hits


def format_hits(hits: Sequence[Hit], *, width: int = 320) -> str:
    if not hits:
        return "未找到结果。"
    lines: list[str] = []
    for rank, hit in enumerate(hits, 1):
        snippet = " ".join(hit.text.split())
        if len(snippet) > width:
            snippet = snippet[:width] + "..."
        lines.append(f"{rank}. [{hit.score:.3f}] {hit.path}  >  {hit.heading}")
        lines.append(f"   {snippet}")
    return "\n".join(lines)


def index_status() -> dict[str, str]:
    if not DB_PATH.is_file():
        return {"status": "missing", "db": str(DB_PATH)}
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    meta = dict(con.execute("SELECT key, value FROM meta"))
    chunks = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    files = con.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    size = DB_PATH.stat().st_size
    con.close()
    return {
        "status": "ready",
        "db": str(DB_PATH),
        "files": str(files),
        "chunks": str(chunks),
        "model": meta.get("model", "?"),
        "updated_at": meta.get("updated_at", "?"),
        "size_mb": f"{size / 1048576:.2f}",
    }


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="rag", description="本地语义检索索引")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_index = sub.add_parser("index", help="构建/增量更新索引")
    p_index.add_argument("--force", action="store_true", help="全量重建")
    p_index.add_argument("--scope", nargs="+", default=["knowledge", "skills"], choices=["knowledge", "skills", "repo"])

    p_search = sub.add_parser("search", help="语义检索")
    p_search.add_argument("query")
    p_search.add_argument("-k", type=int, default=5)
    p_search.add_argument("--scope", default="all", choices=["all", "knowledge", "skills"])
    p_search.add_argument("--json", action="store_true")

    sub.add_parser("status", help="查看索引状态")

    args = parser.parse_args(argv)
    try:
        if args.cmd == "index":
            stats = build_index(tuple(args.scope), force=args.force)
            print(
                f"\n完成：{stats.files_total} 个文件，嵌入 {stats.files_embedded}，"
                f"跳过 {stats.files_skipped}，删除 {stats.files_removed}，"
                f"共 {stats.chunks} 块，用时 {stats.seconds:.1f}s"
            )
        elif args.cmd == "search":
            hits = search_index(args.query, k=args.k, scope=args.scope)
            if args.json:
                print(json.dumps([hit.__dict__ for hit in hits], ensure_ascii=False, indent=1))
            else:
                print(format_hits(hits))
        else:
            print(json.dumps(index_status(), ensure_ascii=False, indent=1))
    except Exception as exc:  # noqa: BLE001 - CLI 边界
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
