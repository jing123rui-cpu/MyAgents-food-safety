# CP-BEV-RM-009：原料包装完整性检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-009
checkpoint_name: 原料包装完整性检查
domain: 原料管理
module: 原料验收
unit: 感官验收
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 3min
```

## ② Inspection Objective

确认原料到达时外包装完好无损，无泄漏、破损、严重变形或污染迹象，保障原料在运输和贮存过程中未被污染。

## ③ Applicable Product

全部饮料品类。适用于所有袋装、桶装、箱装、瓶装原料。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 前往原料仓库或验收区，随机观察 5-10 件原料包装状态 |
| 2 | 现场观察 | 检查包装是否有破损、泄漏、胀袋、虫蛀、霉变 |
| 3 | 现场观察 | 检查包装是否清洁，有无明显污渍或化学品污染痕迹 |
| 4 | 记录核查 | 检查进货查验记录中是否有包装完整性检查的栏目和记录 |
| 5 | 询问 | 询问验收人员：发现包装破损如何处理 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 包装状态现场照片 | 现场照片 | 必须 | 至少 3 张代表性照片 |
| 验收记录（包装检查栏） | 记录拍照 | 可选 | 显示是否有包装检查记录 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 发现包装破损泄漏 | 较大 | 原料可能已被污染 |
| 发现包装胀袋 | 较大 | 可能已微生物繁殖 |
| 包装有明显污渍 | 一般 | 可能在运输中被污染 |
| 验收记录无包装检查栏 | 一般 | 制度设计缺陷 |
| 包装完好但有虫蛀痕迹 | 较大 | 虫害可能已进入包装内部 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 发现破损泄漏或胀袋 | RISK-02 较大风险 |
| 包装污染或虫蛀痕迹但不严重 | RISK-03 一般风险 |
| 包装完好但制度无包装检查要求 | RISK-03 一般风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（原料运输和验收要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 包装完好、无异常 | 符合要求 | 记录为符合 |
| 发现破损但该批尚未使用 | 需要隔离 | 确认企业是否已隔离标识，如已处理则基本符合 |
| 发现包装明显异常但企业已签收入库 | 验收失控 | 判定较大风险 |
| 包装有少量灰尘属正常运输痕迹 | 不属于问题 | 不记录为问题 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-009
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-009-01"
      description: "检查原料件数 | 异常件数 | 异常类型 | 企业处理方式"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-009-001"
      type: "现场照片"
      description: "原料包装现场照片"
  risk_level: "RISK-0X"
  conclusion: "原料包装完整性检查结论描述"
```