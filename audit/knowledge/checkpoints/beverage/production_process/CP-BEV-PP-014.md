# CP-BEV-PP-014：清场

## ① Metadata

```yaml
checkpoint_id: CP-BEV-PP-014
checkpoint_name: 清场
domain: 生产过程管理
module: 生产过程控制
unit: 过程偏差处理
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 8min
```

## ② Inspection Objective

确认生产结束后或换产前的清场操作按规定执行，生产现场无残留物料、无遗留工具、设备清洁彻底，清场记录完整并经过复核确认。

## ③ Applicable Product

全部饮料品类。适用于每班次生产结束或换产前的清场操作。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取清场标准操作规程或清场检查表 |
| 2 | 记录核查 | 从最近一个月选取 5 份清场记录，核对填写完整性 |
| 3 | 现场观察 | 检查生产现场清场后的状态：设备内外、地面、排水沟、工具存放 |
| 4 | 文件核查 | 确认清场记录是否有操作人和复核人签字 |
| 5 | 询问 | 询问操作人员清场检查的项目和标准 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 清场记录（5份） | 记录拍照 | 必须 | 含操作人和复核人签字 |
| 清场SOP或检查表 | 文件扫描 | 必须 | 清场项目和验收标准 |
| 现场清场状态照片 | 拍照 | 可选 | 清场后现场状态 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 清场记录缺失 | 重大 | 无清场记录或记录丢失 |
| 现场发现残留物料或垃圾 | 重大 | 清场不彻底 |
| 清场记录无复核人签字 | 较大 | 清场未经过独立确认 |
| 清场记录提前填写 | 重大 | 生产尚未结束清场记录已填完 |
| 清场项目有遗漏 | 一般 | 部分项目未检查 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 现场发现残留物料或清场记录造假 | RISK-01 重大风险 |
| 无复核签字或清场记录不全 | RISK-02 较大风险 |
| 清场执行但有轻微瑕疵 | RISK-03 一般风险 |
| 清场彻底、记录完整有复核 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（清场管理要求）
- `REG-FOOD-SAFETY-LAW` 条款号（生产过程控制要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 清场记录完整、现场清洁、有复核签字 | 清场管理合规 | 记录为符合 |
| 清场记录显示已完成但现场发现包装材料残留 | 记录与实际不符 | 评估残留物对下一批次的风险 |
| 清场记录中操作人和复核人为同一人 | 复核失效 | 要求企业纠正复核机制 |
| 清场记录的时间在生产结束时间之前 | 记录真实性存疑 | 询问操作人员并确认是否为提前填写 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-PP-014
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-PP-014-01"
      description: "生产线/工序 | 清场项目完整性 | 现场状态 | 复核情况 | 判定"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-PP-014-001"
      type: "记录拍照"
      description: "XX班次清场记录"
  risk_level: "RISK-0X"
  conclusion: "清场结论描述"
```
