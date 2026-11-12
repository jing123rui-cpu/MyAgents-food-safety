# CP-BEV-RM-022：内包材贮存环境检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-022
checkpoint_name: 内包材贮存环境检查
domain: 原料管理
module: 包装材料管理
unit: 包材贮存
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 5min
```

## ② Inspection Objective

确认内包装材料（瓶、盖、膜、标签等）的贮存环境满足清洁、干燥、防尘、防虫的要求，避免包材在使用前受到污染。

## ③ Applicable Product

全部饮料品类。覆盖 PET 瓶、瓶盖、标签、收缩膜、纸箱等包装材料。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 检查包材仓库的整体清洁状况 |
| 2 | 现场观察 | 检查包材是否存放在洁净、干燥的区域 |
| 3 | 现场观察 | 检查包材是否有有效的防尘覆盖 |
| 4 | 现场观察 | 检查包材是否直接暴露在空气中 |
| 5 | 现场观察 | 检查包材仓库的防虫防鼠设施 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 包材仓库环境照片 | 现场照片 | 必须 | 显示整体环境 |
| 包材防尘措施照片 | 现场照片 | 条件必选 | 如有防尘罩或覆盖物 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 包材直接暴露在粉尘环境中 | 较大 | 包材在使用前已受污染 |
| 包材仓库有漏水痕迹 | 较大 | 包材可能受潮 |
| 包材与化学品混放 | 重大 | 存在化学污染风险 |
| 包材无防尘覆盖 | 一般 | 增加污染风险 |
| 包材仓库有虫鼠迹象 | 较大 | 包材可能被啃咬污染 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 与化学品混放 | RISK-01 重大风险 |
| 暴露粉尘或受潮或有虫鼠迹象 | RISK-02 较大风险 |
| 无明显污染但防尘措施不足 | RISK-03 一般风险 |
| 环境清洁干燥有防尘措施 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（包装材料贮存要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 包材仓库清洁、干燥、有防尘 | 符合要求 | 记录为符合 |
| 包材仓库与原料仓库共用 | 可接受 | 确认共用仓库是否满足包材的特殊贮存要求 |
| 包材拆包后剩余部分无防护 | 普遍问题 | 要求企业对已拆包但未使用的包材加防护 |
| 标签与瓶盖在同一区域但分区合理 | 可接受 | 确认是否有有效分区划分 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-022
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-022-01"
      description: "清洁度 | 防尘措施 | 化学品隔离 | 防虫防鼠 | 防潮"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-022-001"
      type: "现场照片"
      description: "内包材贮存环境照片"
  risk_level: "RISK-0X"
  conclusion: "内包材贮存环境检查结论描述"
```