# MyAgents · 食品安全专家

一个可共享、可同步的 Agent 仓库。当前内置 **食品安全专家** Agent，覆盖食品生产企业合规审查、法规标准解读、风险分级、检查前要点分析、整改与监督检查报告撰写。

## 结构

```
MyAgents/
├── .opencode/
│   └── agent/
│       └── food-safety-expert.md        # Agent 定义（OpenCode primary agent）
├── skills/
│   └── food-safety-audit/
│       ├── SKILL.md                     # 检查前风险分析方法论（6 步）
│       ├── workflows/                   # 01~06 分步流程
│       └── references/
│           ├── 检查要点14项.md
│           ├── 食品类别目录.md
│           ├── risk-grading.md          # 风险分级与条款对应
│           └── report-template.md       # 监督检查报告模板
├── scripts/
│   ├── sync.ps1                         # 拉取 / 安装 / 状态
│   └── sync.cmd                         # 双击入口
├── .upstream.json                       # 上游仓库记录（不含凭据）
└── .gitignore
```

## 使用

### 在本目录使用

用 OpenCode 打开 `D:\MyAgents`，切换 agent 到 `food-safety-expert` 即可。项目级 agent 会被自动发现。

### 安装为全局 agent

```powershell
cd D:\MyAgents
.\scripts\sync.ps1 -Install
```

会复制到 `%USERPROFILE%\.config\opencode\agent\`，之后任何目录都能选用。

### 直接对话示例

- 「帮我按 GB 14881 审一下这份车间巡检记录」
- 「这批饮料检出菌落总数超标，帮我定性、分级、写整改要求」
- 「我要去一家小型食用油厂做日常监督检查，先给我检查前分析清单」
- 「这条标签少了 SC 编号，属于第几条，怎么处罚」

## 同步

上游：`https://github.com/caiqfox821/MyAgents-food-safety`（分支 `main`）

```powershell
# 查看状态
.\scripts\sync.ps1 -Status

# 公开仓库直接拉
.\scripts\sync.ps1 -Pull

# 私有仓库：令牌只用于本次命令，不写入 .git/config
$env:GITHUB_TOKEN = "github_pat_xxx"
.\scripts\sync.ps1 -Pull -Token $env:GITHUB_TOKEN
```

拉取策略为 `pull --ff-only`：只做快进合并，本地有改动时不会静默覆盖，冲突会显式失败。

## 首次推送（仓库创建后）

```powershell
cd D:\MyAgents
git init -b main
git add .
git commit -m "feat: 食品安全专家 agent 与检查前分析技能包"
git remote add origin https://github.com/caiqfox821/MyAgents-food-safety.git
git push -u origin main
```

## 免责声明

本仓库内容用于合规分析与审核辅助，不替代监管部门的行政决定，也不替代有资质检验机构的检测结论。法规与标准条款会修订，引用具体限量值前请核实现行有效版本。
