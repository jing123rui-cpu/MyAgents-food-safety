# CP-BEV-RM-020：PET瓶坯验收检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-020
checkpoint_name: PET瓶坯验收检查
domain: 原料管理
module: 包装材料管理
unit: 包材验收
category: beverage
applicable_products: PET瓶装饮料
risk_level: M
priority: P1
estimated_time: 5min
```

## ② Inspection Objective

确认 PET 瓶坯的验收符合企业标准，瓶坯的外观、尺寸、重量、卫生指标等满足生产要求。

## ③ Applicable Product

使用 PET 瓶作为包装容器的饮料产品。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取 PET 瓶坯验收标准或规格书 |
| 2 | 文件核查 | 检查瓶坯进货验收记录 |
| 3 | 现场观察 | 查看瓶坯的外包装是否完好，是否有污染 |
| 4 | 现场观察 | 随机抽取瓶坯观察外观（是否有毛刺、划痕、变色、黑点） |
| 5 | 记录核查 | 检查瓶坯供应商的合格证明文件和检测报告 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 瓶坯验收标准 | 文件扫描 | 必须 | 包括外观、尺寸、重量标准 |
| 瓶坯验收记录 | 记录拍照 | 必须 | 最近批次记录 |
| 瓶坯外观照片 | 现场照片 | 必须 | 显示瓶坯实际状态 |
| 瓶坯检测报告 | 文件扫描 | 可选 | 供应商提供的检测报告 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 瓶坯外观有明显缺陷（毛刺、黑点） | 一般 | 可能影响瓶子的成型和密封 |
| 包装破损导致瓶坯暴露 | 较大 | 瓶坯可能被污染 |
| 无瓶坯验收标准和记录 | 较大 | 包材验收失控 |
| 瓶坯重量不达标 | 一般 | 瓶壁厚度可能不足 |
| 瓶坯标识不清 | 一般 | 无法追溯来源和批号 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 瓶坯包装破损污染且已投入使用 | RISK-02 较大风险 |
| 无验收标准或验收记录 | RISK-02 较大风险 |
| 外观缺陷但不影响使用 | RISK-03 一般风险 |
| 验收标准完善、记录完整 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（包装材料验收要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 有验收标准、记录完整、外观良好 | 符合要求 | 记录为符合 |
| 瓶坯包装破损但企业声称将退回 | 需确认 | 查看隔离区域确认已隔离 |
| 使用回收料生产的瓶坯 | 需关注 | 确认是否使用食品级回收料（PET 食品级回收有严格限制） |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-020
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-020-01"
      description: "验收标准 | 验收记录 | 外观状态 | 包装完整性"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-020-001"
      type: "文件扫描"
      description: "PET瓶坯验收标准"
    - evidence_id: "EVID-RM-020-002"
      type: "现场照片"
      description: "瓶坯外观照片"
  risk_level: "RISK-0X"
  conclusion: "PET瓶坯验收检查结论描述"
```