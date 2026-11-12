# CP-BEV-RM-005：合格供应商名录核查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-005
checkpoint_name: 合格供应商名录核查
domain: 原料管理
module: 供应商管理
unit: 合格供应商名录
category: beverage
applicable_products: 全部饮料
risk_level: H
priority: P0
estimated_time: 5min
```

## ② Inspection Objective

确认企业持有经审批的合格供应商名录，且实际采购原料的供应商均在名录范围内，不存在从合格名录外供应商采购的情况。

## ③ Applicable Product

全部饮料品类。覆盖原辅料、包材的所有采购渠道。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取企业经审批的合格供应商名录文档 |
| 2 | 文件核查 | 确认名录内容包括供应商名称、供应品种、准入日期、有效期 |
| 3 | 文件核查 | 确认名录有审批人签字或电子审批记录 |
| 4 | 交叉核对 | 从进货台账中选取 5 批次原料，核对供应商是否在合格名录中 |
| 5 | 询问 | 询问采购人员：发生紧急采购时如何处理合格名录外供应商 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 合格供应商名录 | 文件扫描 | 必须 | 经审批的当前有效版本 |
| 进货台账（部分记录） | 记录拍照 | 必须 | 用于交叉比对 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 无合格供应商名录 | 重大 | 企业完全依赖口头或记忆管理供应商 |
| 名录未经审批 | 一般 | 有名单但无批准人签字 |
| 实际采购供应商不在名录中 | 重大 | 从非合格供应商处采购原料 |
| 名录内容过期 | 一般 | 名录未更新，关闭的供应商仍在名录上 |
| 名录缺少年度确认标记 | 轻微 | 名录长期未复核 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 无合格名录或发现从非合格供应商采购 | RISK-01 重大风险 |
| 名录存在但覆盖不全或未及时更新 | RISK-02 较大风险 |
| 名录完整且有定期复核机制 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（原料采购管理要求）
- `REG-FOOD-SAFETY-LAW` 条款号（进货查验制度要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 名录完整、审批齐全、交叉比对无异常 | 供应商渠道管控有效 | 记录为符合 |
| 发现 1 批次原料来自名录外供应商 | 立即追溯该批次 | 核查该次采购是否有临时采购审批和补充审核记录 |
| 名录中缺少某关键原料供应商 | 制度执行缺陷 | 确认该原料是否已停用或更换供应商 |
| 名录版本日期距今超过 1 年且无复核标记 | 可能存在失效 | 要求企业确认名录是否需要更新 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-005
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-005-01"
      description: "名录总供应商数 | 交叉比对批次 | 命中率 | 审批状态"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-005-001"
      type: "文件扫描"
      description: "合格供应商名录"
  risk_level: "RISK-0X"
  conclusion: "合格供应商名录核查结论描述"
```