# -*- coding: utf-8 -*-
"""从 audit/knowledge 生成 skills/food-safety-audit/references/knowledge-index.md。

用法（仓库根目录）：
    python scripts/gen_knowledge_index.py

数据来源：
    audit/knowledge/registry/*.yaml          检查点注册表（45 条）
    audit/knowledge/regulations/regulation_registry.yaml  法规注册表
    audit/knowledge/taxonomy/beverage_knowledge_tree.yaml 分类树
"""

from __future__ import annotations

import glob
import os
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("需要 PyYAML：pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.join(ROOT, "audit", "knowledge")
OUT = os.path.join(ROOT, "skills", "food-safety-audit", "references", "knowledge-index.md")

LEVEL_ORDER = ["Critical", "High", "Medium", "Low"]
LEVEL_ZH = {"Critical": "重大", "High": "高", "Medium": "中", "Low": "低"}


def load_checkpoints() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(glob.glob(os.path.join(AUDIT, "registry", "*.yaml"))):
        with open(path, encoding="utf-8") as fh:
            for entry in yaml.safe_load(fh) or []:
                rows.append(entry)
    rows.sort(key=lambda r: r["id"])
    return rows


def load_regulations() -> list[dict]:
    path = os.path.join(AUDIT, "regulations", "regulation_registry.yaml")
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or []


def load_taxonomy() -> dict:
    path = os.path.join(AUDIT, "taxonomy", "beverage_knowledge_tree.yaml")
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("beverage_knowledge_tree", {})


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def build() -> str:
    checkpoints = load_checkpoints()
    regulations = load_regulations()
    tree = load_taxonomy()

    by_domain: dict[str, list[dict]] = {}
    for cp in checkpoints:
        by_domain.setdefault(cp.get("domain", "-"), []).append(cp)

    domain_zh = {}
    for dom in tree.get("domains", []):
        domain_zh[dom["id"]] = dom.get("name_zh") or dom.get("name") or dom["id"]

    domains = [d for d in tree.get("domains", []) if d.get("total_checkpoints")]
    empty_domains = [d for d in tree.get("domains", []) if not d.get("total_checkpoints")]

    parts: list[str] = []
    parts.append("# 引擎知识索引")
    parts.append("")
    parts.append(
        "> 本文件由 `scripts/gen_knowledge_index.py` 从 `audit/knowledge/` 自动生成，请勿手改。"
    )
    parts.append("> 修改知识库后重新运行生成脚本。")
    parts.append("")

    # ── 概览 ─────────────────────────────────────────────
    parts.append("## 1. 概览")
    parts.append("")
    level_counts = {lv: sum(1 for c in checkpoints if c.get("risk_level") == lv) for lv in LEVEL_ORDER}
    parts.append(
        md_table(
            ["资产", "数量", "路径"],
            [
                ["检查点", len(checkpoints), "`audit/knowledge/checkpoints/`"],
                ["风险规则", len(glob.glob(os.path.join(AUDIT, "risk_rules", "**", "*.yaml"), recursive=True)), "`audit/knowledge/risk_rules/`"],
                ["法规条目", len(regulations), "`audit/knowledge/regulations/`"],
                ["分类树子域", sum(len(d.get("sub_domains", [])) for d in tree.get("domains", [])), "`audit/knowledge/taxonomy/beverage_knowledge_tree.yaml`"],
            ],
        )
    )
    parts.append("")
    parts.append(
        "风险等级分布："
        + "，".join(f"{LEVEL_ZH.get(lv, lv)} {level_counts[lv]} 项" for lv in LEVEL_ORDER if level_counts[lv])
        + "。"
    )
    parts.append("")
    parts.append("**当前知识库覆盖范围**：饮料（beverage）制造业，原料管理 25 项 + 生产过程管理 20 项。")
    parts.append("其他食品类别（食用油、方便食品、特殊膳食等）暂无结构化检查点，需按 `workflows/` 方法论人工推导。")
    parts.append("")

    # ── 检查点总表 ────────────────────────────────────────
    parts.append("## 2. 检查点总表（按分类）")
    parts.append("")
    for domain in sorted(by_domain):
        items = by_domain[domain]
        parts.append(f"### {domain_zh.get(domain, domain)}（{len(items)} 项）")
        parts.append("")
        rows = []
        for cp in items:
            laws = "、".join(cp.get("laws") or []) or "-"
            rows.append(
                [
                    f"`{cp['id']}`",
                    cp.get("title", ""),
                    LEVEL_ZH.get(cp.get("risk_level"), cp.get("risk_level", "")),
                    cp.get("subcategory", ""),
                    laws,
                ]
            )
        parts.append(md_table(["ID", "检查点", "风险", "子类", "主要依据"], rows))
        parts.append("")

    # ── 风险规则映射 ─────────────────────────────────────
    parts.append("## 3. 检查点 → 风险规则映射")
    parts.append("")
    parts.append("风险规则文件与检查点一一对应，命名规则 `RR-{检查点ID}.yaml`，判定结果三态：`PASS` / `WARNING` / `FAIL`。下表路径相对 `audit/` 目录。")
    parts.append("")
    rows = []
    for cp in checkpoints:
        cid = cp["id"]
        sub = "production_process" if "PP" in cid else "raw_material"
        rows.append([f"`{cid}`", f"`RR-{cid}.yaml`", f"`knowledge/checkpoints/beverage/{sub}/{cid}.md`"])
    parts.append(md_table(["检查点", "风险规则", "检查点原文"], rows))
    parts.append("")

    # ── 法规清单 ─────────────────────────────────────────
    type_zh = {
        "national_law": "法律",
        "administrative_regulation": "行政法规/规章",
        "national_standard": "国家标准",
        "guideline": "规范性文件",
    }
    parts.append("## 4. 法规清单")
    parts.append("")
    rows = []
    for reg in regulations:
        rows.append(
            [
                f"`{reg['id']}`",
                reg.get("title_zh", ""),
                type_zh.get(reg.get("document_type"), reg.get("document_type", "")),
                reg.get("last_revision") or reg.get("effective_date") or "-",
                "、".join(reg.get("enterprise_types") or []),
            ]
        )
    parts.append(md_table(["ID", "名称", "类型", "施行/修订", "适用企业类型"], rows))
    parts.append("")
    parts.append("适用类型为继承关系：`general_food` → `beverage` → `packaged_water`，子类型自动继承父类型法规。")
    parts.append("")

    # ── 分类树 ───────────────────────────────────────────
    parts.append("## 5. 分类树（有检查点的域）")
    parts.append("")
    for dom in domains:
        parts.append(
            f"### {dom.get('name_zh')}（`{dom['id']}`，{dom.get('total_checkpoints')} 项）"
        )
        parts.append("")
        rows = []
        for sub in dom.get("sub_domains", []):
            cats = []
            cps: list[str] = []
            for cat in sub.get("categories", []):
                cats.append(cat.get("name_zh") or cat.get("name") or cat.get("id"))
                cps.extend(cat.get("checkpoints") or [])
            rows.append(
                [
                    sub.get("name_zh") or sub.get("name") or sub.get("id"),
                    "、".join(cats) or "-",
                    "、".join(f"`{c}`" for c in cps) or "-",
                ]
            )
        parts.append(md_table(["子域", "类别", "检查点"], rows))
        parts.append("")
    if empty_domains:
        parts.append("### 已定义但暂无检查点的域")
        parts.append("")
        parts.append("、".join(f"{d.get('name_zh')}（`{d['id']}`）" for d in empty_domains))
        parts.append("")
        parts.append("这些域是知识库的扩展位置；在补齐检查点前，涉及这些主题时按 `workflows/` 与法规原文人工分析。")
        parts.append("")

    # ── 使用顺序 ─────────────────────────────────────────
    parts.append("## 6. 检索顺序")
    parts.append("")
    parts.append("1. 先在本索引按关键词定位检查点 ID（如「供应商许可证」→ `CP-BEV-RM-001`）。")
    parts.append("2. 读 `audit/knowledge/checkpoints/.../{ID}.md` 取检查目的、方法、证据要求、常见发现项、AI 指导。")
    parts.append("3. 读 `audit/knowledge/risk_rules/.../RR-{ID}.yaml` 取判定逻辑与风险等级。")
    parts.append("4. 读 `audit/knowledge/regulations/{REG-ID}.md` 取条款细节。")
    parts.append("5. 需要批量/过滤检索时用 CLI：")
    parts.append("")
    parts.append("```bash")
    parts.append("cd audit")
    parts.append("python main.py inspect --query supplier      # 用英文关键词，避免 Windows 中文参数转码")
    parts.append("python main.py inspect --id CP-BEV-RM-001")
    parts.append("python main.py inspect --risk High")
    parts.append("```")
    parts.append("")
    parts.append("详见 `references/audit-cli.md`。")
    parts.append("")

    return "\n".join(parts)


def main() -> None:
    content = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    print(f"written {OUT} ({len(content)} chars)")


if __name__ == "__main__":
    main()
