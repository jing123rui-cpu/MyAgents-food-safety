# CP-BEV-RM-014：原料仓库防虫防鼠设施检查

## ① Metadata

```yaml
checkpoint_id: CP-BEV-RM-014
checkpoint_name: 原料仓库防虫防鼠设施检查
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

确认原料仓库的防虫防鼠设施配置到位且运行正常，有效防止虫鼠进入仓库污染原料。

## ③ Applicable Product

全部饮料品类。覆盖所有原料仓库和贮存区域。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 检查仓库门口的挡鼠板是否安装、高度是否足够（≥60cm） |
| 2 | 现场观察 | 检查仓库窗户是否有纱窗，是否完好 |
| 3 | 现场观察 | 检查仓库内部是否有虫鼠活动迹象（鼠粪、鼠咬痕、虫迹） |
| 4 | 现场观察 | 检查仓库墙角、管道穿墙处是否有封堵 |
| 5 | 现场观察 | 检查灭蝇灯是否正常亮灯、位置是否合理 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 挡鼠板照片 | 现场照片 | 必须 | 显示安装位置和高度 |
| 仓库内部虫鼠迹象照片 | 现场照片 | 条件必选 | 如发现迹象则拍照 |
| 灭蝇灯运行状态照片 | 现场照片 | 可选 | 显示灭蝇灯是否正常 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 无挡鼠板或挡鼠板高度不够 | 较大 | 鼠类可轻易进入 |
| 仓库内发现鼠粪/鼠咬痕 | 重大 | 实际已有鼠患 |
| 发现虫迹或虫尸 | 较大 | 虫害控制失效 |
| 墙面/管道孔洞未封堵 | 一般 | 潜在的进入通道 |
| 纱窗破损 | 一般 | 蚊虫可能进入 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 发现鼠患迹象 | RISK-01 重大风险 |
| 防鼠设施缺失或虫害迹象 | RISK-02 较大风险 |
| 个别设施不完善但无虫鼠迹象 | RISK-03 一般风险 |
| 设施完善、无虫鼠迹象 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（防虫防鼠设施要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 挡鼠板、纱窗、封堵全部到位，无虫鼠迹象 | 符合要求 | 记录为符合 |
| 发现少量鼠粪 | 立即拍照 | 判定重大风险，同时检查原料是否有被鼠咬痕迹 |
| 有挡鼠板但高度不足 60cm | 硬件不达标 | 要求企业加高挡鼠板，判定基本符合 |
| 企业声称使用了电子驱鼠器 | 需查证 | 电子驱鼠器不能替代物理防鼠设施，应要求同时使用挡鼠板 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-RM-014
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-RM-014-01"
      description: "挡鼠板 | 纱窗 | 孔洞封堵 | 虫鼠迹象 | 灭蝇灯"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-RM-014-001"
      type: "现场照片"
      description: "仓库防虫防鼠设施照片"
  risk_level: "RISK-0X"
  conclusion: "原料仓库防虫防鼠设施检查结论描述"
```