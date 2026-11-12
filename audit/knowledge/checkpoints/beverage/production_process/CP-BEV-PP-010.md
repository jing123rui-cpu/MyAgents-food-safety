# CP-BEV-PP-010：产品标识

## ① Metadata

```yaml
checkpoint_id: CP-BEV-PP-010
checkpoint_name: 产品标识
domain: 生产过程管理
module: 生产过程控制
unit: 过程记录
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 8min
```

## ② Inspection Objective

确认生产过程中的原料、半成品、成品均附有清晰、正确的标识，标识内容包含产品名称、批号、数量、状态（待检/合格/不合格）等信息。

## ③ Applicable Product

全部饮料品类。适用于生产全过程的物料标识管理。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 检查生产现场各物料容器（原料桶、半成品罐、成品箱）的标识情况 |
| 2 | 现场观察 | 检查标识内容是否完整（品名、批号、数量、日期、状态） |
| 3 | 现场观察 | 检查待检/合格/不合格区域的物料是否状态标识明确 |
| 4 | 文件核查 | 查看标识管理相关规定或作业指导书 |
| 5 | 询问 | 询问操作人员物料状态发生变化时如何更新标识 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 现场标识照片 | 拍照 | 必须 | 至少 5 个不同物料的标识 |
| 标识管理规定/指导书 | 文件扫描 | 可选 | 企业标识管理规范 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 物料无任何标识 | 重大 | 无法识别物料信息和状态 |
| 标识内容不完整 | 较大 | 缺少批号、状态等关键信息 |
| 待检区与合格区物料混放且无标识区分 | 重大 | 存在误用未检验物料的风险 |
| 标识未随物料状态更新 | 较大 | 物料已检验但标识仍为待检 |
| 标识方式不统一 | 一般 | 不同区域标识格式不一致 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 物料无标识或状态区域混放 | RISK-01 重大风险 |
| 标识内容不完整或未及时更新 | RISK-02 较大风险 |
| 标识存在但格式不统一 | RISK-03 一般风险 |
| 标识清晰完整、状态明确 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（物料标识管理要求）
- `REG-FOOD-SAFETY-LAW` 条款号（追溯管理要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 所有物料标识清晰完整、状态明确 | 标识管理合规 | 记录为符合 |
| 物料有标识但缺少批号 | 可追溯性缺陷 | 确认是否有其他方式（如电子系统）可追溯 |
| 合格区中混有待检物料 | 存在使用风险 | 要求立即隔离，调查是否有误用情况 |
| 标识已模糊不清但物料信息可从其他途径获取 | 标识维护问题 | 建议企业建立标识更换频次规范 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-PP-010
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-PP-010-01"
      description: "物料名称 | 标识完整性 | 状态标识 | 一致性 | 判定"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-PP-010-001"
      type: "现场拍照"
      description: "XX物料标识照片"
  risk_level: "RISK-0X"
  conclusion: "产品标识结论描述"
```
