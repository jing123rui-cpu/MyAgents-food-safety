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
├── .opencode/agent/food-safety-expert.md    # 食品安全专家 Agent（primary）
├── skills/food-safety-audit/                # 检查前风险分析方法论
│   ├── SKILL.md
│   ├── workflows/01~06
│   └── references/{检查要点14项,食品类别目录,risk-grading,report-template}
├── audit/                                   # 食品安全审核引擎（迁移自 Food-Audit-Agent）
│   ├── main.py                              # CLI 入口
│   ├── script/                              # 检索、规则引擎、工作流、AI、报告导出
│   ├── knowledge/                           # 检查点、法规、风险规则、分类树
│   ├── api/ · web/                          # FastAPI 与页面
│   ├── skills/                              # 引擎侧 8 个技能（yaml）
│   ├── docs/ · reports/ · tests/
│   └── pyproject.toml · requirements.txt
├── scripts/sync.ps1                         # 拉取 / 安装 / 状态
├── .upstream.json                           # 上游记录（不含凭据）
└── .gitignore
```

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
python main.py health                 # 知识库加载状态
python main.py inspect --id CP-BEV-RM-001
python main.py inspect --query 原料验收 --risk High
python -m api.server                  # Web/API（见 audit/docs）
```

可选：设置 `DEEPSEEK_API_KEY` 启用 AI 分析；不设置时检索、规则、工作流仍可离线运行。

## 同步

上游：`https://github.com/caiqfox821/MyAgents-food-safety`（`main`）

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

## 免责声明

用于合规分析与审核辅助，不替代监管部门的行政决定，也不替代有资质检验机构的检测结论。法规与标准会修订，引用具体条款和限量值前请核实现行有效版本。
