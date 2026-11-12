# 语义检索（semantic_search）

**状态**：已实现 · **阶段**：0 - 知识定位

## 用途

把口语化的提问（「供货方资质过期了会怎么定性」「杀菌记录缺了几天算严重吗」）直接召回最相关的检查点、风险规则、法规与技能文档，解决关键词检索「换个说法就查不到」的问题。

只做**召回**，不产出结论：命中结果必须回到原文核对，不能拿相似度当合规判定依据。

## 引擎实现

| 组件 | 路径 | 职责 |
|---|---|---|
| 索引与检索 | `audit/script/rag.py` | 切块、嵌入、SQLite 索引、混合打分 |
| CLI 入口 | `audit/main.py` | `index` / `search` / `rag-status` 子命令 |
| 索引文件 | `audit/.index/rag.db` | 本地 SQLite，**不入库**（`.gitignore`） |
| 嵌入模型 | paratera `GLM-Embedding-2` | 1024 维，OpenAI 兼容 `/v1/embeddings` |

不依赖向量数据库：向量以 BLOB 存 SQLite，检索时读入内存做矩阵点积（约 850 块、几 MB），只用 numpy。

## 索引范围

| 来源 | 内容 |
|---|---|
| `audit/knowledge/` | 检查点 `.md`、风险规则 `.yaml`、法规、分类树 |
| `skills/food-safety-audit/` | 方法论、能力说明、reference 文档 |
| `AGENTS.md`、`README.md` | 仓库级说明（scope `repo`） |

`references/knowledge-index.md` 不索引，避免索引行淹没结果。

## 输入 / 输出

- 输入：自然语言问题、`-k`（返回条数）、`--scope all|knowledge|skills`
- 输出：`[{score, path, heading, text}]`，按混合分排序，**同一文件最多 2 条**，避免单篇文档刷屏

混合分 = `0.65 × 余弦相似度 + 0.35 × 关键词覆盖率`（中文按 2 字滑窗切词）。纯向量对短查询、专有名词（`CP-BEV-RM-001`、`GB 7101`）偏弱，关键词项负责兜底。

## 在对话中的用法

```bash
cd audit
python main.py search "供应商许可证过期" -k 5
python main.py search "杀菌温度记录缺失" -k 3 --scope knowledge
python main.py search "报告怎么写" --scope skills
```

拿到 `path` 后按 `heading` 定位章节，再读原文。典型动作：

1. 用户问题模糊 → `search` 召回 3~5 条，挑出最相关的 `CP-BEV-xxx` / `RR-*` / `REG-*`。
2. 用 `inspect --id <ID>` 或直接读文件，取「判定逻辑 / 法条依据 / 常见发现项」原文。
3. 需要引用的条款、限量值以原文为准，相似度只用于排序。

## 索引维护

```bash
cd audit
python main.py rag-status          # 文件数、块数、模型、大小、更新时间
python main.py index               # 增量：只嵌入改动过的文件
python main.py index --force       # 全量重建
```

- 首次建库或知识库大改后跑一次全量：约 130 文件 / 850 块，约 47 秒（3 并发批处理）。
- 日常改动只重建变更文件；切块逻辑变化由 `CHUNK_VERSION` 触发自动全量。
- 嵌入模型为外部 API，离线时无法建库/检索；已建好的索引不联网也能读，但查询本身仍需一次嵌入调用。

## 密钥

不写入仓库。读取顺序：

1. 环境变量 `PARATERA_API_KEY`
2. `~/.local/share/opencode/auth.json` 中对应 provider 的 `key`

可选覆盖：`PARATERA_EMBEDDING_URL`、`PARATERA_EMBEDDING_MODEL`、`PARATERA_EMBEDDING_WORKERS`。

## 局限

- 只覆盖已入库的知识：饮料（原料管理 25 + 生产过程 20）。其他类别召回的是方法论，不是专用检查点。
- 语义相似 ≠ 条款适用：可能召回主题相近但类别不符的规则，必须人工确认适用范围。
- 索引会过期：知识库改了但没重建，检索结果仍是旧内容。改完知识库记得跑 `index`。
- 中文短查询（2~5 字）区分度有限，尽量带上场景词（「供应商许可证 过期 定性」比「许可证」好）。
