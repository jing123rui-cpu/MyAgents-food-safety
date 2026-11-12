# 引擎 CLI 使用说明

引擎位于仓库 `audit/`，与 Agent 技能包共用同一套知识库。以下命令均在仓库根目录执行。

## 0. 前置

```bash
cd audit
python -c "import yaml; print(yaml.__version__)"   # 需要 PyYAML
# 缺失时：pip install -r requirements.txt
```

`health` 会在未设置 `DEEPSEEK_API_KEY` 时打印一条 WARNING，属正常；检索、规则、工作流全部离线可用。语义检索（`index` / `search`）需要 `PARATERA_API_KEY` 或本机 auth.json，见第 3 节。

## 1. 命令总览

| 命令 | 作用 | 是否写文件 |
|---|---|---|
| `python main.py health` | 知识库加载状态 | 否 |
| `python main.py inspect --id <ID>` | 按检查点 ID 查 | 否 |
| `python main.py inspect --query <关键词>` | 关键词检索 | 否 |
| `python main.py inspect --category <类别>` | 按类别过滤 | 否 |
| `python main.py inspect --risk <等级>` | 按风险等级过滤 | 否 |
| `python main.py search <问题>` | 语义检索（RAG） | 否（需联网嵌入） |
| `python main.py index` | 建/更新语义索引 | **是**（`audit/.index/rag.db`） |
| `python main.py rag-status` | 语义索引状态 | 否 |
| `python demo_export.py` | 导出 Word 报告 | **是** |
| `python demo_writing.py` | 生成报告文本 | **是** |
| `python demo_inspection_ai.py` | AI 检查演示（需 API Key） | **是** |
| `uvicorn api.server:app --port 8000` | 启动 API 服务 | 否 |

## 2. 常用示例

```bash
# 知识库健康检查：期望 READY，注册 45 / 检查点 46 / 规则 45 / 分类树 270
python main.py health

# 精确查单个检查点（最稳定，不受中文编码影响）
python main.py inspect --id CP-BEV-RM-001

# 关键词检索：用注册表里的英文关键词更可靠
python main.py inspect --query supplier
python main.py inspect --query "process parameter"

# 按风险等级筛：High 应有 29 项，Medium 16 项
python main.py inspect --risk High

# 组合过滤
python main.py inspect --category 原料管理 --risk High
```

## 3. 语义检索（RAG）

关键词检索换个说法就查不到，语义检索用自然语言召回检查点、风险规则、法规与技能文档。

```bash
# 查索引状态：文件数、块数、模型、大小、更新时间
python main.py rag-status

# 语义检索，默认返回 5 条
python main.py search "供应商许可证过期" -k 5
python main.py search "杀菌温度记录缺失" -k 3 --scope knowledge
python main.py search "报告怎么写" --scope skills
python main.py search "菌落总数超标怎么定性" --json
```

**输出含义**

```
1. [0.639] audit/knowledge/risk_rules/beverage/raw_material/RR-CP-BEV-RM-001.yaml  >  RR-CP-BEV-RM-001 · 供应商生产许可证审查
   id: RR-CP-BEV-RM-001 checkpoint_id: CP-BEV-RM-001 title: 供应商生产许可证审查 ...
```

- 方括号为混合分：`0.65 × 余弦相似度 + 0.35 × 关键词覆盖率`，只用于排序，不是合规判定依据。
- 同一文件最多 2 条，避免一篇文档占满结果。
- `--scope`：`all`（默认）/ `knowledge`（知识库）/ `skills`（技能文档）。

**建库与更新**

```bash
python main.py index               # 增量：只嵌入改动过的文件
python main.py index --force       # 全量重建
python main.py index --scope knowledge
```

首次建立索引：约 130 个文件、850 块，约 47 秒（3 并发批处理）。日常改完知识库跑一次 `index` 即可；切块逻辑变更由 `CHUNK_VERSION` 自动触发全量重建。索引文件在 `audit/.index/rag.db`，已加入 `.gitignore`，不随仓库同步。

**密钥与配置**

嵌入模型为 paratera `GLM-Embedding-2`（1024 维）。密钥按顺序读取，不写入仓库：

1. 环境变量 `PARATERA_API_KEY`
2. `~/.local/share/opencode/auth.json` 中对应 provider 的 `key`

可选环境变量：`PARATERA_EMBEDDING_URL`、`PARATERA_EMBEDDING_MODEL`、`PARATERA_EMBEDDING_WORKERS`（默认 3）。

**注意**：建库与查询都要调用嵌入 API，离线不可用；索引建好后可离线读取，但每次查询仍需一次嵌入请求。语义检索只负责召回，引用条款前必须回到原文核对。

## 4. 输出字段

```
Checkpoint:   CP-BEV-RM-001          检查点 ID
Title:        供应商生产许可证审查      检查点名称
Domain:       原料管理
Module:       供应商管理
Objective:    检查目的（截断 80 字）
Category:     原料管理                注册表类别
Subcategory:  供应商资质审核
Risk Level:   High                   注册表风险等级
Evidence Req: 供应商生产许可证复印件    必需证据
Laws:         食品生产许可管理办法, 食品安全法
Risk Rule:    RR-CP-BEV-RM-001 (Critical)   对应规则及规则等级
Condition:    许可证复印件与原件一致且在有效期内
```

`Risk Level` 与规则里的 `risk_level` 可能不同（注册表为 High，规则为 Critical），以规则等级作为判定口径，注册表等级用于筛选。

## 5. 编码注意事项（Windows PowerShell 5.1）

- 控制台中文乱码是代码页问题，**文件内容本身是 UTF-8**，不影响结果。
- 中文参数经 PowerShell 传参可能被转成 GBK 而匹配失败。建议：
  - 优先用 `--id`；
  - 关键词用注册表中的英文词（`supplier`、`license`、`temperature`、`traceability`）；
  - 或先 `chcp 65001` / 设 `$env:PYTHONUTF8=1` 再执行。
- `python ... 2>&1` 会把 WARNING 当作错误流，PowerShell 因此显示 `Exited with code 1`，但 Python 实际返回 0。判断成功与否看输出内容，不要只看退出码。

## 6. 何时需要 API Key

| 能力 | 无 Key | 有 Key |
|---|---|---|
| health / inspect | 完整可用 | 完整可用 |
| 规则判定 | 完整可用 | 完整可用 |
| 语义检索 / 建索引 | **不可用** | 完整可用 |
| 整改建议文本 | 模板文本 | AI 生成 |
| 报告正文 | 模板文本 | AI 生成 |

```bash
# PowerShell
$env:DEEPSEEK_API_KEY = "..."
$env:PARATERA_API_KEY = "..."      # 仅语义检索需要
# bash
export DEEPSEEK_API_KEY="..."
export PARATERA_API_KEY="..."
```

Key 只从环境变量（或本机 auth.json）读取，不要写进仓库文件。

## 7. 使用纪律

1. `inspect` / `search` / `rag-status` 是只读查询，可放心执行。
2. `index` 会写 `audit/.index/rag.db`；首次全量约 47 秒，执行前说明。
3. `demo_*.py` 会写文件，执行前先说明输出目录，执行后报告文件路径。
4. 引擎结果是辅助判定，重大风险必须人工复核（见 `references/risk-grading.md`）。
5. 知识库当前只覆盖饮料的原料管理与生产过程；其他类别不要用 `inspect` 结果反推结论。
6. 语义检索只做召回，命中后必须回到原文；相似度高不代表条款适用。

## 8. 相关文档

- 知识库结构与检索顺序：`references/knowledge-index.md`
- 原 8 项引擎能力 + 语义检索：`capabilities/README.md`、`capabilities/semantic-search.md`
- 引擎自身文档：`audit/README.md`、`audit/docs/`
