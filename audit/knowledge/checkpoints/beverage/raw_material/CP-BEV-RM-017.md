# CP-BEV-RM-017：原料离墙离地存放检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-017
checkpoint_name: 原料离墙离地存放检查
domain: 原料管理
module: 原料贮存
unit: 库存管理
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 3min
```

## ② Inspection Objective

确认原料存放时与墙壁和地面保持规定距离，便于通风、清洁和虫害控制，防止原料受潮或受到墙壁冷凝水污染。

## ③ Applicable Product

全部饮料品类。覆盖原料仓库中所有袋装、箱装、桶装原料。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 检查原料是否直接放置在地面上（应使用垫仓板） |
| 2 | 现场观察 | 检查原料堆垛与墙壁之间的距离是否足够（通常 ≥ 20cm） |
| 3 | 现场观察 | 检查原料与天花板之间是否有足够空间 |
| 4 | 现场观察 | 检查原料与照明灯具之间是否有安全距离 |
| 5 | 现场观察 | 检查通道是否畅通，便于检查和搬运 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 原料离墙离地存放照片 | 现场照片 | 必须 | 至少 2 张，不同角度 |
| 原料直接落地照片 | 现场照片 | 条件必选 | 如发现直接落地的情况 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 原料直接放在地面上 | 较大 | 易受潮、虫鼠易接触 |
| 原料紧贴墙壁 | 一般 | 不利于通风和检查 |
| 堆垛过高靠近天花板 | 一般 | 影响消防喷淋效果 |
| 通道堵塞 | 一般 | 不利于日常检查 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 原料直接落地 | RISK-02 较大风险 |
| 紧贴墙壁或堆垛不规范 | RISK-03 一般风险 |
| 全部离墙离地、堆码规范 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（原料存放要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 全部使用垫仓板、离墙 ≥ 20cm | 符合要求 | 记录为符合 |
| 部分原料直接落地但为刚卸货暂放 | 需确认 | 确认是否临时堆放，如已超过 24 小时则判定不符合 |
| 用木板替代垫仓板 | 基本符合 | 木质垫板易滋生虫害，建议企业更换塑料或金属垫板 |
| 距离墙壁 5-10cm | 基本符合 | 介于合规和不合规之间，记录为基本符合 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-017
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-017-01"
      description: "垫仓板使用率 | 离墙距离 | 堆码高度合规性 | 通道畅通性"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-017-001"
      type: "现场照片"
      description: "原料离墙离地存放照片"
  risk_level: "RISK-0X"
  conclusion: "原料离墙离地存放检查结论描述"
```