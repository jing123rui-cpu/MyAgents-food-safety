# CP-BEV-RM-013：原料仓库温湿度控制检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-013
checkpoint_name: 原料仓库温湿度控制检查
domain: 原料管理
module: 原料贮存
unit: 仓库条件
category: beverage
applicable_products: 全部饮料
risk_level: H
priority: P0
estimated_time: 5min
```

## ② Inspection Objective

确认原料仓库的温湿度控制在规定范围内，有温湿度监控设备并定期记录，温湿度异常时有处理机制。

## ③ Applicable Product

全部饮料品类。特别关注有温湿度要求的原料（冷藏原料、浓缩果汁、奶粉、香精等）。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 查看原料仓库是否安装温湿度计，位置是否合理 |
| 2 | 现场观察 | 记录当前温湿度读数 |
| 3 | 记录核查 | 调取最近 1 个月的温湿度监控记录 |
| 4 | 记录核查 | 检查温湿度是否在企业规定的范围内 |
| 5 | 记录核查 | 检查温湿度异常记录及处置情况 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 当前温湿度计读数照片 | 现场照片 | 必须 | 显示温湿度计实时数据 |
| 最近 1 个月温湿度记录 | 记录拍照 | 必须 | 显示连续监控数据 |
| 温湿度异常处置记录 | 文件扫描 | 可选 | 如有异常则提供 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 仓库无温湿度监控设备 | 重大 | 无法控制贮存条件 |
| 温湿度记录缺失严重 | 较大 | 长期不记录或不连续 |
| 温湿度超出规定范围 | 较大 | 可能影响原料质量 |
| 温湿度记录显示长期不达标但未处理 | 重大 | 管理失控 |
| 温湿度计未校准 | 一般 | 数据不可靠 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 无监控设备或长期不达标未处理 | RISK-01 重大风险 |
| 有设备但记录不连续或超限未及时处置 | RISK-02 较大风险 |
| 记录完整但有少量超限且已处理 | RISK-03 一般风险 |
| 温湿度全程合规 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（贮存温湿度控制要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 有设备、有记录、数据达标 | 符合要求 | 记录为符合 |
| 无温湿度计但仓库条件良好 | 硬件缺失 | 判定不符合，要求加装 |
| 记录连续但有 1-2 次超限且有处置 | 基本符合 | 记录为基本符合 |
| 记录数据整齐划一（如每天完全相同） | 记录疑似造假 | 比对不同位置的温度计读数，扩大核查 |
| 冷藏库温度记录显示停机期间温度升高 | 需关注 | 检查停机是否有通知，产品是否评估 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-013
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-013-01"
      description: "监控设备状态 | 记录连续性 | 温湿度达标率 | 异常处置率"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-013-001"
      type: "现场照片"
      description: "仓库温湿度计读数"
    - evidence_id: "EVID-RM-013-002"
      type: "记录拍照"
      description: "温湿度监控记录"
  risk_level: "RISK-0X"
  conclusion: "原料仓库温湿度控制检查结论描述"
```