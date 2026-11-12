# CP-BEV-RM-016：原料库存标识检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-016
checkpoint_name: 原料库存标识检查
domain: 原料管理
module: 原料贮存
unit: 库存管理
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 5min
```

## ② Inspection Objective

确认库存原料的标识齐全、清晰、准确，包括品名、批号、生产日期、保质期、数量、库存状态（合格/待检/不合格）等信息。

## ③ Applicable Product

全部饮料品类。覆盖所有原料仓库中的食品原料和包材。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 在原料仓库中随机选取 5-10 个不同品种的原料 |
| 2 | 现场观察 | 检查每个原料的标识卡片或标签是否完整 |
| 3 | 现场观察 | 确认标识是否包含：品名、批号、生产日期、保质期、入库日期、数量、状态 |
| 4 | 现场观察 | 确认标识是否清晰可读，有无脱落或污损 |
| 5 | 现场观察 | 查看是否有"待检""合格""不合格"状态标识 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 库存标识照片（3-5 张） | 现场照片 | 必须 | 覆盖不同品种和区域 |
| 无标识原料照片 | 现场照片 | 条件必选 | 如发现无标识原料 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 原料完全无标识 | 较大 | 无法识别原料信息 |
| 标识信息不全 | 一般 | 缺少生产日期、保质期或批号 |
| 标识与实物不一致 | 较大 | 标识信息与实际不符 |
| 无状态标识（合格/待检） | 一般 | 不清楚原料是否可以投入使用 |
| 标识脏污脱落 | 一般 | 标识维护不到位 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 无标识或标识与实物不符 | RISK-02 较大风险 |
| 标识信息不全或状态标识缺失 | RISK-03 一般风险 |
| 标识齐全清晰 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（原料标识管理要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 所有检查的原料均有完整清晰标识 | 符合要求 | 记录为符合 |
| 发现无标识原料堆垛 | 立即查明 | 确认是否已验收，如已验收则要求立即补标 |
| 标识信息显示批号相同但包装日期不同 | 可疑 | 可能不同批次混装，要求核实 |
| 标识上状态为"合格"但该原料尚未完成检验 | 管理混乱 | 判定不符合，要求查清是否未经检验投入使用 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-016
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-016-01"
      description: "抽查原料数 | 标识完整率 | 标识准确率 | 状态标识覆盖率"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-016-001"
      type: "现场照片"
      description: "原料库存标识照片"
  risk_level: "RISK-0X"
  conclusion: "原料库存标识检查结论描述"
```