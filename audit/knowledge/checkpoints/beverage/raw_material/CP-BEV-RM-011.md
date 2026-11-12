# CP-BEV-RM-011：不合格原料隔离与标识检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-011
checkpoint_name: 不合格原料隔离与标识检查
domain: 原料管理
module: 原料验收
unit: 不合格原料处理
category: beverage
applicable_products: 全部饮料
risk_level: H
priority: P0
estimated_time: 5min
```

## ② Inspection Objective

确认企业对验收不合格的原料进行了有效隔离和清晰标识，防止误用。

## ③ Applicable Product

全部饮料品类。适用于所有经判定为不合格的原料。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取不合格原料台账，查看近期不合格记录 |
| 2 | 现场观察 | 到原料仓库查看是否有专门的不合格品存放区域 |
| 3 | 现场观察 | 确认不合格品存放区域是否有明确标识 |
| 4 | 现场观察 | 确认不合格品是否与合格品有效隔离 |
| 5 | 文件核查 | 检查不合格品的处置记录（退货/报废/降级使用） |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 不合格品区现场照片 | 现场照片 | 必须 | 显示隔离区域和标识 |
| 不合格原料台账 | 记录拍照 | 必须 | 近期不合格记录 |
| 不合格品处置记录 | 文件扫描 | 可选 | 退货或报废凭证 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 无专门不合格品存放区域 | 较大 | 不合格品无固定隔离场所 |
| 不合格品与合格品混放 | 重大 | 存在误用高风险 |
| 不合格品有隔离但无标识 | 一般 | 无法区分不合格品的品种和数量 |
| 不合格品台账缺失 | 较大 | 无法追溯不合格品的来源和去向 |
| 不合格品长期未处置 | 一般 | 积压的不合格品占用区域且过期 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 不合格品与合格品混放 | RISK-01 重大风险 |
| 无隔离区或无台账 | RISK-02 较大风险 |
| 有隔离有台账但标识不清晰 | RISK-03 一般风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（不合格品管理要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 不合格品专区、标识清晰、台账完整 | 符合要求 | 记录为符合 |
| 无不合格品台账但声称近期无不合格 | 需核实 | 核查近期进货记录是否有异常批次 |
| 不合格品与合格品在同一区域但用围栏分隔 | 基本符合 | 检查分隔是否有效，标识是否清晰 |
| 不合格品与合格品完全混放 | 直接判定 | 重大风险，拍照固定证据 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-011
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-011-01"
      description: "隔离区域 | 标识清晰度 | 台账完整性 | 处置及时性"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-011-001"
      type: "现场照片"
      description: "不合格品隔离区照片"
    - evidence_id: "EVID-RM-011-002"
      type: "记录拍照"
      description: "不合格原料台账"
  risk_level: "RISK-0X"
  conclusion: "不合格原料隔离与标识检查结论描述"
```