# CP-BEV-RM-019：食品添加剂专库/专柜检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-019
checkpoint_name: 食品添加剂专库/专柜检查
domain: 原料管理
module: 原料贮存
unit: 特殊原料管理
category: beverage
applicable_products: 全部饮料
risk_level: H
priority: P0
estimated_time: 5min
```

## ② Inspection Objective

确认食品添加剂实行专库/专柜存放，有专人管理，标识清晰，防止误用和滥用。

## ③ Applicable Product

全部饮料品类。适用于所有使用食品添加剂的企业。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 检查添加剂是否有专用的存放区域（专库/专柜） |
| 2 | 现场观察 | 确认专库/专柜是否上锁并有专人管理 |
| 3 | 现场观察 | 检查添加剂容器上的标识是否清晰（名称、生产日期、保质期、开瓶日期） |
| 4 | 现场观察 | 检查是否与其他原料混放 |
| 5 | 记录核查 | 检查添加剂领用记录 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 添加剂专库/专柜照片 | 现场照片 | 必须 | 显示存放区域和上锁情况 |
| 添加剂标识照片 | 现场照片 | 必须 | 显示名称和有效期 |
| 添加剂领用记录 | 记录拍照 | 可选 | 显示领用情况 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 添加剂与普通原料混放 | 重大 | 极易发生误用 |
| 无专库/专柜 | 较大 | 未遵守专管要求 |
| 专柜未上锁 | 一般 | 管控不严 |
| 添加剂无标识或标识不清 | 一般 | 容易混淆 |
| 容器上的名称与实际内容物不符 | 重大 | 存在误用风险 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 与普通原料混放或容器内容不符 | RISK-01 重大风险 |
| 无专库/专柜 | RISK-02 较大风险 |
| 有专柜但有管理不到位（未上锁、标识不清） | RISK-03 一般风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（添加剂贮存要求）
- `REG-FOOD-ADDITIVE` 条款号（添加剂管理要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 专库/专柜、上锁、标识清晰、有领用记录 | 符合要求 | 记录为符合 |
| 有专柜但未上锁 | 管理缺陷 | 要求立即整改，记录为基本符合 |
| 添加剂放在开放式货架上但与其他原料分区 | 基本符合 | 确认是否确有物理隔离，如只有空间距离则要求加锁 |
| 添加剂标识为"A"但内容物颜色气味不匹配 | 可疑 | 立即停止使用该添加剂，要求企业确认 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-019
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-019-01"
      description: "专库/专柜 | 上锁 | 标识完整性 | 领用记录 | 混放情况"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-019-001"
      type: "现场照片"
      description: "食品添加剂存放区域照片"
  risk_level: "RISK-0X"
  conclusion: "食品添加剂专库/专柜检查结论描述"
```