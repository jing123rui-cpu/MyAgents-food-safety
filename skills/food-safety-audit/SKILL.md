---
name: food-safety-audit
description: 食品生产/经营企业合规审查技能包。融合 6 步检查前分析方法论（企业信息→类别→工艺→法规→历史→检查重点）与可运行的审核引擎能力（45 个检查点、45 条风险规则、12 部法规、报告导出）。用于检查前风险研判、法规条款定位、问题定性与风险分级、整改要求与监督检查报告撰写。
---

# 食品安全合规审查（方法论 + 引擎）

## 定位

一套技能包，两种用法：

| 用途 | 主导内容 | 产出 |
|---|---|---|
| **进场前**：这家企业该重点查什么 | `workflows/01~06` 方法论 | 检查前分析清单 |
| **进场后**：这些问题怎么定性、怎么写 | `capabilities/` 引擎能力 + 知识库 | 判定结果、整改要求、检查报告 |

两者共用同一套业务口径，路径都在本仓库内，不依赖外部绝对路径。

## 知识底座

```
skills/food-safety-audit/
├── SKILL.md                  ← 本文件（总入口）
├── workflows/01~06           ← 六步方法论（人工分析）
├── capabilities/             ← 八项引擎能力（结构化处理）
└── references/
    ├── knowledge-index.md    ← 45 检查点 / 45 规则 / 12 法规 / 分类树（自动生成）
    ├── audit-cli.md          ← 引擎命令行用法
    ├── 检查要点14项.md        ← 监督检查要点与高风险类别
    ├── 食品类别目录.md        ← 类别与法规文件映射
    ├── risk-grading.md       ← 四级风险分级与《食品安全法》条款对应
    └── report-template.md    ← 报告骨架与自查清单

audit/                        ← 引擎与结构化知识库
├── knowledge/checkpoints/    ← 检查点原文（16 节 Schema v2）
├── knowledge/risk_rules/     ← 风险规则（PASS/WARNING/FAIL）
├── knowledge/regulations/    ← 法规注册表与条款全文
├── knowledge/taxonomy/       ← 食品分类树
└── script/                   ← 检索、规则引擎、工作流、AI、报告导出
```

**覆盖范围**：结构化知识目前为饮料制造业（原料管理 25 项 + 生产过程管理 20 项）。其他食品类别按方法论推导，并标注「知识库未覆盖」。

## 能力矩阵

| # | 能力 | 状态 | 何时用 |
|---|---|---|---|
| 1 | [检查点匹配](capabilities/checkpoint-match.md) | 已实现 | 把口头/文字描述映射到 `CP-BEV-xxx` |
| 2 | [法规检索](capabilities/regulation-lookup.md) | 已实现 | 按类别取适用法规与条款 |
| 3 | [风险评估](capabilities/risk-assessment.md) | 已实现 | 按规则判定符合性、定级 |
| 4 | [检查编排](capabilities/inspection-review.md) | 已实现 | 一次取全某主题的结构化信息 |
| 5 | [企业评价](capabilities/enterprise-evaluation.md) | 已实现 | 汇总逐项结果为总体结论 |
| 6 | [整改建议](capabilities/corrective-action.md) | 已实现 | 写整改要求（五要素） |
| 7 | [报告生成](capabilities/report-generation.md) | 已实现 | 出 12 节报告与 docx |
| 8 | [图像识别](capabilities/image-recognition.md) | 规划中 | 照片/扫描件（**当前不可用**） |

## 路径 A：检查前分析（6 步）

```
01 企业基本信息 → 02 食品类别 → 03 生产工艺风险 → 04 法规标准匹配 → 05 历史风险 → 06 检查重点
```

| 步骤 | 文件 | 核心产出 |
|---|---|---|
| 01 | `workflows/01-企业基本信息分析.md` | 资质状态、规模倾向、属地信息 |
| 02 | `workflows/02-食品类别识别.md` | 类别判定、许可一致性、法规目录 |
| 03 | `workflows/03-生产工艺风险分析.md` | 高风险工序、关键控制点 |
| 04 | `workflows/04-法规标准匹配.md` | 适用法规与重点条款 |
| 05 | `workflows/05-历史风险信息分析.md` | 历史问题聚类、复发风险 |
| 06 | `workflows/06-检查重点生成.md` | 14 项要点关注等级 + 证据清单 |

每一步输出是下一步输入；第 6 步汇总为检查前分析清单（格式见文末）。

## 路径 B：检查后判定（引擎流水线）

```
检查点匹配 → 法规检索 → 风险评估 → 企业评价 → 整改建议 → 报告生成
   (1)         (2)         (3)         (5)         (6)         (7)
```

配套只读查询（在 `audit/` 下执行，详见 [audit-cli.md](references/audit-cli.md)）：

```bash
python main.py health                      # READY / 45 / 46 / 45 / 270
python main.py inspect --id CP-BEV-RM-001
python main.py inspect --query supplier
python main.py inspect --risk High
```

## 检索顺序（不要凭记忆补条款）

1. 在 `references/knowledge-index.md` 按关键词定位检查点 ID。
2. 读 `audit/knowledge/checkpoints/.../{ID}.md`：检查目的、方法、证据要求、常见发现项、AI 指导。
3. 读 `audit/knowledge/risk_rules/.../RR-{ID}.yaml`：判定逻辑、等级、法条依据。
4. 读 `audit/knowledge/regulations/REG-*.md`：条款细节。
5. 知识库没有的（标签、污染物、致病菌、农残等），按通用知识回答并标 `【需核对原文】`。

## 输出规范

**检查前分析清单**

```markdown
# 检查前分析清单

## 一、企业概况
- 企业名称 / 食品类别 / 许可状态 / 企业规模 / 属地

## 二、风险概况
| 风险维度 | 判断 | 依据 |
|---|---|---|
| 资质风险 | 高/中/低 | |
| 工艺风险 | | |
| 类别固有风险 | | |
| 历史问题风险 | | |

## 三、检查重点（按优先级）
| 优先级 | 检查要点 | 关注理由 | 建议核查证据 |
|---|---|---|---|

## 四、建议调取资料
## 五、待确认事项（【需现场确认】）
```

**不符合项**（四段式，缺一不可）

```markdown
- 事实：{单位 + 时间 + 地点 + 行为/状态 + 证据}
- 依据：《食品安全法》第 X 条；GB XXXXX 第 X.X 条
- 等级：重大 / 高 / 中 / 低（危害 × 可能性 × 波及范围）
- 处置：{立即措施} + {纠正措施} + {验证方式}
```

## 判断原则

1. **类别固有风险优先**：特殊膳食 > 饮料（蛋白/果蔬汁）> 方便食品 > 食用油，再用工艺修正。
2. **历史问题加权**：同类问题二次出现，关注等级至少上调一级。
3. **规模修正**：小型/微型企业在人员管理、自查、记录追溯上默认加强关注。
4. **证据导向**：每条关注点必须落到「查什么资料、看什么现场」。
5. **未出厂可降级**：同一定性，未出厂比已流通低一级；特殊食品反向从严。

## 边界

- 输出「检查前分析清单」时不写检查结论；只有拿到证据后才做定性。
- 不编造条款号与限量值；不确定就标注待核对。
- 不替代监管部门决定，不替代有资质机构的检验结论。
- 不把推荐性标准（GB/T）当作处罚依据。
- 图片当前无法识别，收到照片时要求文字补充关键信息。

## 维护

知识库变更后重新生成索引：

```bash
python scripts/gen_knowledge_index.py
```

新增检查点/规则时，沿用 `audit/knowledge/checkpoints/CHECKPOINT_SCHEMA_V2.md` 的 16 节结构与 `RR-{检查点ID}.yaml` 命名，并同步 `knowledge/registry/` 与分类树，否则 `health` 会出现告警。
