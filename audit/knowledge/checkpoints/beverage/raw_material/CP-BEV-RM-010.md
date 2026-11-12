# CP-BEV-RM-010：原料保质期与生产日期核对

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-010
checkpoint_name: 原料保质期与生产日期核对
domain: 原料管理
module: 原料验收
unit: 感官验收
category: beverage
applicable_products: 全部饮料
risk_level: H
priority: P0
estimated_time: 3min
```

## ② Inspection Objective

确认验收记录的原料生产日期和保质期信息准确，实际到货的剩余保质期符合企业规定的验收要求，不存在过期或临近过期原料入库的情况。

## ③ Applicable Product

全部饮料品类。特别关注保质期短的原料（如乳原料、果汁、冷藏原料）。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 记录核查 | 从进货台账中选取 5 批次原料，查看记录的生产日期和保质期 |
| 2 | 现场核对 | 到仓库现场核对同批次原料包装上的实际生产日期和保质期 |
| 3 | 记录核查 | 核对企业原料验收标准中是否有剩余保质期比例要求 |
| 4 | 现场核对 | 检查库存中的原料是否有超过保质期的情况 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 进货台账（生产日期/保质期栏） | 记录拍照 | 必须 | 显示记录的生产日期信息 |
| 库存原料包装生产日期照片 | 现场照片 | 必须 | 实际包装上的日期信息 |
| 企业验收标准（剩余保质期要求） | 文件扫描 | 可选 | 若有制度要求则提供 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 库存中发现过期原料 | 重大 | 存在使用过期原料的风险 |
| 验收记录日期与实际不一致 | 较大 | 记录造假或录入错误 |
| 原料入库时已临近过期 | 一般 | 剩余保质期不满足企业内控要求 |
| 无剩余保质期验收标准 | 一般 | 制度不完善 |
| 未记录生产日期和保质期 | 较大 | 记录缺失关键信息 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 库存中发现过期原料 | RISK-01 重大风险 |
| 记录日期与实际不符或未记录保质期 | RISK-02 较大风险 |
| 入库时剩余保质期短但未过期 | RISK-03 一般风险 |
| 日期准确、无过期原料 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-FOOD-SAFETY-LAW` 条款号（禁止使用过期原料）
- `REG-GB-14881` 条款号（原料保质期管理要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 记录日期与实物一致且在保质期内 | 符合要求 | 记录为符合 |
| 库存中发现过期原料但已隔离 | 基本符合 | 检查隔离标识是否清晰，处置记录是否完整 |
| 库存有过期原料且与正常原料混放 | 重大违规 | 立即判定重大风险，拍照固定证据 |
| 记录日期与实物相差较大 | 可疑 | 扩大抽查批次，判断是否系统性记录问题 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-010
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-010-01"
      description: "抽查批次 | 记录与实物一致性 | 过期情况 | 剩余保质期合规性"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-010-001"
      type: "记录拍照"
      description: "进货台账生产日期/保质期记录"
    - evidence_id: "EVID-RM-010-002"
      type: "现场照片"
      description: "原料包装生产日期实拍"
  risk_level: "RISK-0X"
  conclusion: "原料保质期与生产日期核对结论描述"
```