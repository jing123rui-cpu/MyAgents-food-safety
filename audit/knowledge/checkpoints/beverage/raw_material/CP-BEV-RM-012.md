# CP-BEV-RM-012：原料退货/让步接收记录检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-012
checkpoint_name: 原料退货/让步接收记录检查
domain: 原料管理
module: 原料验收
unit: 不合格原料处理
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 5min
```

## ② Inspection Objective

确认企业对验收不合格的原料有明确的退货或让步接收流程，让步接收时经过了风险评估和审批，记录完整。

## ③ Applicable Product

全部饮料品类。适用于出现验收不合格但采取退货或让步接收处理的原料。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取不合格原料台账，查看不合格原料的处理方式记录 |
| 2 | 文件核查 | 如有让步接收记录，检查让步接收的审批流程 |
| 3 | 文件核查 | 检查让步接收是否有风险评估报告或说明 |
| 4 | 文件核查 | 检查退货是否有退货记录和物流凭证 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 让步接收审批记录 | 文件扫描 | 条件必选（有让步接收时） | 含风险评估和审批签字 |
| 退货记录 | 文件扫描 | 条件必选（有退货时） | 含退货日期和物流凭证 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 让步接收无任何审批 | 较大 | 未经评估直接使用不合格原料 |
| 让步接收审批人不是有权限人员 | 一般 | 审批人不具备审批资格 |
| 不合格原料长期堆放未退货也未报废 | 一般 | 处置不及时 |
| 退货无记录 | 一般 | 无法证明原料已退回供应商 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 让步接收未经审批直接使用 | RISK-02 较大风险 |
| 让步接收有审批但风险评估不充分 | RISK-03 一般风险 |
| 有完整退货/让步接收流程和记录 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（不合格原料处理要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 无不合格原料记录且企业确认无不合格情况 | 不存在处理需求 | 记录为不适用 |
| 有不合格记录且处理记录完整 | 符合要求 | 记录为符合 |
| 有让步接收但无审批签字 | 程序违规 | 判定较大风险 |
| 让步接收的缺陷涉及食品安全指标 | 不能让步 | 涉及食品安全指标的不合格原料原则上不应让步接收 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-012
  status: "OK / NOK / NA / PENDING"
  findings:
    - finding_id: "FIND-RM-012-01"
      description: "不合格批次数量 | 让步接收批次数 | 退货批次数 | 审批完整性"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-012-001"
      type: "文件扫描"
      description: "让步接收/退货记录"
  risk_level: "RISK-0X"
  conclusion: "原料退货/让步接收记录检查结论描述"
```