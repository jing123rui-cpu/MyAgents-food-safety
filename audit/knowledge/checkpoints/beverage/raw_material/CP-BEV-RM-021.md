# CP-BEV-RM-021：瓶盖密封性检验检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-021
checkpoint_name: 瓶盖密封性检验检查
domain: 原料管理
module: 包装材料管理
unit: 包材验收
category: beverage
applicable_products: 全部饮料
risk_level: H
priority: P0
estimated_time: 5min
```

## ② Inspection Objective

确认企业对瓶盖等密封件进行了必要的验收检验（外观、尺寸、密封性测试），确保瓶盖能够有效密封产品。

## ③ Applicable Product

全部饮料品类。适用于所有使用瓶盖、罐盖等密封件的产品。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取瓶盖验收标准，检查是否有密封性测试要求 |
| 2 | 记录核查 | 检查瓶盖进货验收记录，是否有密封性测试结果 |
| 3 | 现场观察 | 查看瓶盖贮存环境是否清洁干燥 |
| 4 | 人员询问 | 询问品控人员：瓶盖密封性测试的检测方法和频率 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 瓶盖验收标准 | 文件扫描 | 必须 | 含密封性测试要求 |
| 瓶盖验收记录（含密封性测试结果） | 记录拍照 | 必须 | 显示检测结果 |
| 瓶盖贮存环境照片 | 现场照片 | 可选 | 显示贮存条件 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 无瓶盖密封性检验 | 较大 | 无法确保封口质量 |
| 瓶盖贮存环境脏污 | 较大 | 瓶盖可能被污染 |
| 瓶盖验收记录缺少尺寸检测 | 一般 | 尺寸不合格可导致密封不良 |
| 不同供应商瓶盖混放 | 一般 | 可能混淆不同规格 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 无密封性检验或检验发现不合格仍使用 | RISK-02 较大风险 |
| 有检验但频率不足或项目不全 | RISK-03 一般风险 |
| 检验项目齐全、记录完整 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（包装材料验收要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 有密封性检验记录且合格 | 符合要求 | 记录为符合 |
| 企业称使用自动在线扭矩检测替代来料检验 | 可接受 | 确认在线检测的校准和验证记录 |
| 瓶盖贮存区域无防尘措施 | 基本符合 | 建议增加防尘罩 |
| 瓶盖检验记录长期全部合格（数据异常一致） | 可能未真实检测 | 要求企业现场演示检测过程 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-021
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-021-01"
      description: "密封性检验 | 贮存环境 | 检测频率 | 检验记录完整性"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-021-001"
      type: "文件扫描"
      description: "瓶盖验收标准"
    - evidence_id: "EVID-RM-021-002"
      type: "记录拍照"
      description: "瓶盖验收记录"
  risk_level: "RISK-0X"
  conclusion: "瓶盖密封性检验检查结论描述"
```