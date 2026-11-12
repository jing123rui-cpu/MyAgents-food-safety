# 风险评估（risk_assessment）

**状态**：已实现 · **阶段**：3 - 风险判定

## 用途

对每条证据按对应风险规则判定符合性，输出状态、分值、理由、违反法规与建议。

## 引擎实现

| 组件 | 路径 | 职责 |
|---|---|---|
| 规则引擎 | `audit/script/rule_engine.py` | 确定性判定，无 AI |
| 规则库 | `audit/knowledge/risk_rules/**/RR-*.yaml` | 45 条规则，与检查点一一对应 |
| 数据模型 | `audit/script/models.py` | `Evidence`、`EvaluationResult` |

**判定逻辑**：定位证据对应规则 → 校验证据完整性与描述质量 → 按严重程度检查附件要求 → 返回结构化结果。

## 规则文件结构（示例 `RR-CP-BEV-RM-001.yaml`）

```yaml
id: RR-CP-BEV-RM-001
checkpoint_id: CP-BEV-RM-001
risk_level: Critical
decision_logic:
  - condition: 许可证复印件与原件一致且在有效期内
    result: PASS
  - condition: 许可证已过期但企业声称正在办理续期
    result: WARNING
    severity: Medium
required_evidence: [供应商生产许可证复印件]
pass_condition: ...
fail_condition: ...
legal_basis: [REG-PRODUCE-MEASURE, REG-FOOD-SAFETY-LAW]
```

## 输入 / 输出

- 输入：`evidence`（证据项，含描述与附件）、`matched_checkpoints`
- 输出：`evaluation_results`（`COMPLIANT` / `NON_COMPLIANT` / `NOT_APPLICABLE`，含分值、理由、违反法规、建议）、`statistics`（符合/不符合/重大风险/一般风险计数）

## 三态含义

| 状态 | 含义 | 后续动作 |
|---|---|---|
| `COMPLIANT` | 证据满足通过条件 | 记录，不展开 |
| `NON_COMPLIANT` | 命中失败条件 | 进入整改建议与报告 |
| `NOT_APPLICABLE` | 该检查点不适用于本企业 | 说明理由，不计入分母 |

## 在对话中的用法

1. 先把用户给的证据按检查点归位（见 [检查点匹配](checkpoint-match.md)）。
2. 读对应 `RR-*.yaml`，逐条对照 `decision_logic`，说明命中哪一条。
3. 规则未覆盖的情形，用 `references/risk-grading.md` 的四级分级（重大/高/中/低）人工判定，并标注「规则外判定」。
4. 输出四段式：事实 → 条款 → 等级 → 处置。

## 局限

- 严重程度阈值硬编码；Critical / High 规则要求附件，缺附件会判为证据不足。
- 规则只覆盖饮料的原料与生产过程两类域。
- 引擎结果是指南性判定，重大风险必须人工复核。
