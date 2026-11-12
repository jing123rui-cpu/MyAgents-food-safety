# CP-BEV-RM-004：供应商年度评价记录检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-004
checkpoint_name: 供应商年度评价记录检查
domain: 原料管理
module: 供应商管理
unit: 供应商评价
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 5min
```

## ② Inspection Objective

确认企业已按制度要求对合格供应商进行定期（年度）评价，评价内容包括供货质量、交货及时性、资质有效性等，并形成评价结论。

## ③ Applicable Product

全部饮料品类。适用于所有已准入的合格供应商。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取企业供应商年度评价制度，确认评价频率和标准 |
| 2 | 文件核查 | 调取最近一个年度的供应商评价记录 |
| 3 | 文件核查 | 确认评价是否覆盖全部合格供应商 |
| 4 | 文件核查 | 检查评价内容是否包括质量表现、交货表现、资质有效期等维度 |
| 5 | 文件核查 | 检查评价不合格的供应商是否有整改或淘汰记录 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 供应商年度评价记录 | 文件扫描 | 必须 | 最近年度的评价记录 |
| 评价不合格供应商的处置记录 | 文件扫描 | 可选 | 整改通知、淘汰记录等 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 未进行年度评价 | 较大 | 合格供应商名录更新但无年度评价记录 |
| 评价覆盖不全 | 一般 | 部分供应商未纳入年度评价 |
| 评价内容流于形式 | 一般 | 评价表填写简单，无数据支撑 |
| 评价不合格无后续处置 | 较大 | 评价得分低但未采取任何措施 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 连续两年未进行年度供应商评价 | RISK-02 较大风险 |
| 有评价但覆盖不全或评价不合格未处置 | RISK-03 一般风险 |
| 评价完整且不合格供应商已处置 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（供应商管理要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 年度评价报告完整，不合格供应商有处置记录 | 制度执行有效 | 记录为符合 |
| 有评价记录但未覆盖全部供应商 | 执行缺陷 | 核查未评价供应商是否仍在供货，如是则升级 |
| 评价得分低的供应商仍在正常供货且无记录 | 制度形同虚设 | 判定为较大风险 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-004
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-004-01"
      description: "评价年度 | 被评价供应商数 | 合格名录总数 | 评价覆盖率"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-004-001"
      type: "文件扫描"
      description: "供应商年度评价汇总记录"
  risk_level: "RISK-0X"
  conclusion: "供应商年度评价记录检查结论描述"
```