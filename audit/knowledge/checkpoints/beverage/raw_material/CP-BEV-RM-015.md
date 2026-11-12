# CP-BEV-RM-015：原料先进先出执行检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-015
checkpoint_name: 原料先进先出执行检查
domain: 原料管理
module: 原料贮存
unit: 库存管理
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 8min
```

## ② Inspection Objective

确认企业建立了原料先进先出（FIFO）管理制度，并在实际库存管理中有效执行，防止原料因长期存放导致过期变质。

## ③ Applicable Product

全部饮料品类。特别关注有保质期要求的原料。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取企业原料贮存管理制度，检查是否有 FIFO 规定 |
| 2 | 现场观察 | 查看仓库中同品种不同批次的原料堆放位置 |
| 3 | 现场观察 | 确认较早批次的原料是否放置在取用侧 |
| 4 | 记录核查 | 查看领料记录中批次的取用顺序是否与入库顺序一致 |
| 5 | 询问 | 询问仓管人员：如何确保先进先出执行 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 原料堆放现场照片 | 现场照片 | 必须 | 显示批次摆放位置 |
| 领料记录（部分） | 记录拍照 | 必须 | 显示批次取用顺序 |
| 仓库管理制度 | 文件扫描 | 可选 | 查看制度是否规定 FIFO |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 无 FIFO 管理制度 | 一般 | 制度不完善 |
| 较早批次被压在较晚批次下方 | 一般 | 实际未执行 FIFO |
| 领料记录显示批次跳跃 | 一般 | 未按入库顺序领用 |
| 仓管人员不了解 FIFO 要求 | 较大 | 人员培训不足 |
| 较早批次已过期仍在库中 | 重大 | FIFO 完全失效 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 较早批次过期仍未被领用（FIFO 完全失效） | RISK-02 较大风险 |
| 批次存放顺序不合理但未导致过期 | RISK-03 一般风险 |
| 制度完善、现场堆放合理、记录可验证 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（原料贮存管理要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 堆放顺序合理且领料记录验证一致 | 符合要求 | 记录为符合 |
| 堆放顺序不合理但未造成过期 | 执行不到位 | 判定基本符合，要求立即整改 |
| 企业使用电子 WMS 系统自动管控 FIFO | 系统管控 | 查看系统截图验证功能是否启用 |
| 不同批次混放无法区分 | 库存管理混乱 | 判定不符合，要求改进标识管理 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-015
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-015-01"
      description: "制度覆盖 | 现场堆放合理性 | 领料记录验证 | FIFO 执行率"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-015-001"
      type: "现场照片"
      description: "原料堆放位置照片"
    - evidence_id: "EVID-RM-015-002"
      type: "记录拍照"
      description: "原料领料记录"
  risk_level: "RISK-0X"
  conclusion: "原料先进先出执行检查结论描述"
```