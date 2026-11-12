# AGENTS.md

本仓库是**食品安全专家 Agent** 的可同步工作区，两层结构：Agent 层（`.opencode/agent/` + `skills/`）与引擎层（`audit/`）。两层共享同一套业务口径。

## 目录

| 位置 | 作用 |
|---|---|
| `.opencode/agent/food-safety-expert.md` | 食品安全专家 Agent（primary），人格、边界、工作方法 |
| `skills/food-safety-audit/SKILL.md` | 技能包总入口：路径 A 检查前 / 路径 B 检查后 |
| `skills/food-safety-audit/workflows/01~06` | 检查前六步方法论 |
| `skills/food-safety-audit/capabilities/` | 8 项引擎能力 + 语义检索说明 |
| `skills/food-safety-audit/references/` | 知识索引、CLI 用法、风险分级、报告模板 |
| `audit/knowledge/` | 检查点、风险规则、法规、分类树、注册表 |
| `audit/script/` | 检索、规则引擎、工作流、AI、报告导出、RAG |
| `audit/.index/rag.db` | 本地语义索引（生成物，已 gitignore） |
| `scripts/gen_knowledge_index.py` | 由知识库重新生成 `references/knowledge-index.md` |

## 常用命令

```powershell
cd audit
python main.py health                 # 期望 READY / 45 / 46 / 45 / 270
python main.py inspect --id CP-BEV-RM-001
python main.py inspect --query supplier --risk High
python main.py search "供应商许可证过期" -k 5   # 语义检索，需 PARATERA_API_KEY
python main.py index                  # 增量更新语义索引；--force 全量
python main.py rag-status
```

知识库改动后同步更新两个索引：

```powershell
python scripts\gen_knowledge_index.py
cd audit; python main.py index
```

## 约定

1. **能查就不猜**：检查点、条款、判定逻辑先读 `audit/knowledge/`，再作答。
2. **语义检索只做召回**：`search` 结果必须回到原文核对，不能拿相似度当判定依据。
3. **不编造条款与限量值**：不确定标 `【需核对原文】`；区分强制（GB）与推荐（GB/T）。
4. **知识库覆盖有限**：结构化检查点目前只覆盖饮料（原料管理 25 + 生产过程 20），其他类别按方法论推导并标注「知识库未覆盖」。
5. **密钥不入库**：`DEEPSEEK_API_KEY`、`PARATERA_API_KEY` 只从环境变量或本机 `~/.local/share/opencode/auth.json` 读取。
6. **索引不入库**：`audit/.index/` 是本地生成物，不提交；换机器后跑一次 `python main.py index` 重建。
7. **Windows 编码**：中文参数可能被 PowerShell 转码，优先用 `--id` 或英文关键词；必要时 `$env:PYTHONIOENCODING="utf-8"`。

## 同步

```powershell
.\scripts\sync.ps1 -Pull                       # 拉取（--ff-only）
.\scripts\sync.ps1 -Push                       # 提交所有改动并推送
.\scripts\sync.ps1 -Push -Message "feat: ..."  # 指定提交信息
.\scripts\sync.ps1 -Status                     # 状态与远端
```

`origin` 使用 SSH（`git@github.com:...`），配置一次后不需要 PAT。`-Push` 会 `git add -A` 后提交，提交前会打印待提交清单；`.gitignore` 已排除密钥、虚拟环境与本地索引。

## 改动纪律

- 新增检查点/规则时沿用 `audit/knowledge/checkpoints/CHECKPOINT_SCHEMA_V2.md` 的 16 节结构与 `RR-{检查点ID}.yaml` 命名，并同步 `audit/knowledge/registry/` 与分类树，否则 `health` 会告警。
- 改切块逻辑要提升 `audit/script/rag.py` 的 `CHUNK_VERSION`，触发索引全量重建。
- 提交信息用 `feat:` / `fix:` / `docs:` / `chore:` 前缀，中文描述。
