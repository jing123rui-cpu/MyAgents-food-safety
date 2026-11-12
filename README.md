# MyAgents · 食品安全专家

可共享、可同步的食品安全 Agent 仓库。分两层：

| 层 | 位置 | 作用 |
|---|---|---|
| **Agent 层** | `.opencode/agent/` + `skills/` | 给大模型用的专家人格、方法论、报告模板 |
| **引擎层** | `audit/` | 可运行的食品安全审核引擎（知识库 + 检索 + 风险规则 + 报告导出 + CLI/API/Web） |

两层共享同一套业务口径：Agent 负责研判、解释、写作，引擎负责结构化知识与规则计算。

## 结构

```
MyAgents/
├── AGENTS.md                                # 仓库级约定（结构、命令、边界）
├── .opencode/agent/food-safety-expert.md    # 食品安全专家 Agent（primary）
├── skills/food-safety-audit/                # 技能包：方法论 + 能力说明 + 索引
│   ├── SKILL.md                             # 总入口（路径 A 检查前 / 路径 B 检查后）
│   ├── workflows/01~06                      # 六步检查前分析
│   ├── capabilities/                        # 8 项引擎能力 + 语义检索（checkpoint-match … semantic-search）
│   └── references/
│       ├── knowledge-index.md               # 45 检查点 / 45 规则 / 12 法规 / 分类树（自动生成）
│       ├── audit-cli.md                     # 引擎命令行用法
│       ├── 检查要点14项.md · 食品类别目录.md
│       └── risk-grading.md · report-template.md
├── audit/                                   # 食品安全审核引擎（迁移自 Food-Audit-Agent）
│   ├── main.py                              # CLI 入口（health / inspect / search / index / rag-status）
│   ├── script/                              # 检索、规则引擎、工作流、AI、报告导出、RAG
│   ├── knowledge/                           # 检查点、法规、风险规则、分类树、注册表
│   ├── .index/rag.db                        # 本地语义索引（工作区生成，不入库）
│   ├── api/ · web/                          # FastAPI 与页面
│   ├── skills/                              # 引擎侧 8 个技能定义（yaml）
│   ├── docs/ · reports/ · tests/
│   └── pyproject.toml · requirements.txt
├── scripts/
│   ├── sync.ps1                             # 拉取 / 安装 / 状态
│   └── gen_knowledge_index.py               # 由知识库重新生成 knowledge-index.md
├── .upstream.json                           # 上游记录（不含凭据）
└── .gitignore
```

## 融合方式

技能包不是引擎的说明文档，而是**同一套业务口径的两面**：

| 场景 | 走哪条 | 用到什么 |
|---|---|---|
| 进场前：这家企业该查什么 | `workflows/01~06` | 企业信息、类别、工艺、法规、历史风险、14 项要点 |
| 进场后：问题怎么定性 | `capabilities/1→2→3→5` | 检查点匹配 → 法规检索 → 规则判定 → 企业评价 |
| 写整改与报告 | `capabilities/6→7` | 五要素整改、12 节报告、docx 导出 |
| 查条款/检查点 | `references/knowledge-index.md` + `audit/knowledge/` | 先索引定位，再读原文 |
| 描述模糊、关键词查不到 | 能力 9 语义检索 | `python main.py search "<问题>"` 召回候选，再核对原文 |

结构化知识目前覆盖饮料（原料管理 25 项 + 生产过程管理 20 项），其他食品类别按方法论推导并标注未覆盖。

## 使用

### 1. Agent

在 OpenCode 中打开本目录，选择 `food-safety-expert`；或安装到全局：

```powershell
.\scripts\sync.ps1 -Install
```

对话示例：
- 「按 GB 14881 审一下这份车间巡检记录」
- 「饮料菌落总数超标，定性、分级、写整改要求」
- 「小型食用油厂日常监督检查，先给检查前分析清单」

### 2. 引擎

```powershell
cd audit
python main.py health                 # READY / 45 / 46 / 45 / 270
python main.py inspect --id CP-BEV-RM-001
python main.py inspect --query supplier --risk High
uvicorn api.server:app --port 8000    # Web/API（见 audit/docs）
```

语义检索（可选，需要 `PARATERA_API_KEY` 或本机 auth.json）：

```powershell
cd audit
python main.py index                  # 建/更新索引，首建约 47 秒
python main.py search "供应商许可证过期" -k 5
python main.py rag-status
```

索引为本地 SQLite（`audit/.index/rag.db`，约 130 文件 / 850 块），不随仓库同步；嵌入模型 paratera `GLM-Embedding-2`（1024 维）。

可选：设置 `DEEPSEEK_API_KEY` 启用 AI 分析；不设置时检索、规则、工作流仍可离线运行（语义检索除外）。

知识库更新后重新生成索引与语义索引：

```powershell
python scripts\gen_knowledge_index.py
cd audit
python main.py index
```

## 同步

上游：`https://github.com/jing123rui-cpu/MyAgents-food-safety`（`main`）

```powershell
.\scripts\sync.ps1 -Status
.\scripts\sync.ps1 -Pull                  # 公开仓库
$env:GITHUB_TOKEN = "github_pat_xxx"; .\scripts\sync.ps1 -Pull -Token $env:GITHUB_TOKEN
```

`--ff-only`：只做快进合并，本地有改动时显式失败，不静默覆盖。

## 迁移说明

`audit/` 由 `D:\2026年\Food-Audit-Agent` 的工作区版本迁入（233 个文件，排除 `.git`、`__pycache__`、`.pytest_cache`）。
原项目历史提交未随迁（原仓库工作区有 117 项未提交改动，以工作区为准）；如需保留历史，可后续用 `git subtree` 重建。

`skills/food-safety-audit/` 来自 `D:\2026年\食品行业合规性检测要求生成器\skills\`，原文件已保留与本仓库一致的口径。

融合内容：`capabilities/` 将 `audit/skills/*/skill.yaml` 的 8 项引擎能力转写为可读说明（输入/输出/引擎位置/对话用法/局限），并补充语义检索能力（第 9 项）；`references/knowledge-index.md` 由知识库自动生成，提供检查点、规则、法规、分类树的统一检索入口；`SKILL.md` 改为「检查前方法论 + 检查后引擎流水线」双路径总入口。

语义检索层：`audit/script/rag.py` 提供本地 RAG，嵌入走 paratera `GLM-Embedding-2`，向量存 SQLite，不引入向量数据库。只做召回，不替代条款原文。

## 免责声明

用于合规分析与审核辅助，不替代监管部门的行政决定，也不替代有资质检验机构的检测结论。法规与标准会修订，引用具体条款和限量值前请核实现行有效版本。
