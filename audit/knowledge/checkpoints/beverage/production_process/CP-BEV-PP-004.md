# CP-BEV-PP-004：物料转移

## ① Metadata

```yaml
checkpoint_id: CP-BEV-PP-004
checkpoint_name: 物料转移
domain: 生产过程管理
module: 生产过程控制
unit: 工艺参数监控
category: beverage
applicable_products: 全部饮料
risk_level: M
priority: P1
estimated_time: 8min
```

## ② Inspection Objective

确认生产过程中原料、半成品、成品在各工序间的转移操作规范，防止交叉污染、混料和标识丢失，确保物料可追溯。

## ③ Applicable Product

全部饮料品类。适用于各工序间的物料转移操作。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 现场观察 | 观察物料转移操作，检查容器标识是否清晰、完整 |
| 2 | 文件核查 | 查看物料转移记录或交接单，核对品名、数量、日期 |
| 3 | 现场观察 | 检查转移容器是否专用、清洁，有无交叉污染风险 |
| 4 | 询问 | 询问操作人员不同物料转移时的区分措施 |
| 5 | 现场观察 | 检查暂存区域的物料是否分区存放且有明确标识 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 物料转移/交接记录 | 记录拍照 | 必须 | 至少 3 份交接记录 |
| 工序转移台账 | 文件扫描 | 可选 | 完整的物料流向记录 |
| 容器清洁记录 | 拍照 | 可选 | 转移容器的清洗消毒记录 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 转移容器无标识或标识不清 | 较大 | 无法识别容器内物料信息 |
| 不同物料共用容器未清洗 | 重大 | 存在交叉污染风险 |
| 转移记录缺失或数据不一致 | 较大 | 数量或品名与实际情况不符 |
| 暂存区域物料混放 | 较大 | 不同品种/批次物料未分区存放 |
| 转移过程无防污染措施 | 一般 | 敞口转运无防护罩 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 未清洗容器导致交叉污染 | RISK-01 重大风险 |
| 标识缺失或转移记录不一致 | RISK-02 较大风险 |
| 物料暂存不规范但可追溯 | RISK-03 一般风险 |
| 物料转移规范、标识清晰完整 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（物料储存和转运要求）
- `REG-FOOD-SAFETY-LAW` 条款号（生产过程控制要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 容器标识清晰、转移记录完整 | 物料管控合规 | 记录为符合 |
| 发现容器无标识但操作人员能口头说明内容物 | 标识管理缺陷 | 要求立即补签，评估是否需要追溯 |
| 发现不同批次物料混放在同一区域 | 批次管理问题 | 确认是否有物理隔离措施 |
| 转移记录数量与实际盘点明显不符 | 可能存在物料损失 | 进一步追溯差异原因 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-PP-004
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-PP-004-01"
      description: "转移工序 | 容器标识状态 | 记录核对结果 | 交叉污染评估"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-PP-004-001"
      type: "现场观察"
      description: "物料转移操作观察记录"
  risk_level: "RISK-0X"
  conclusion: "物料转移结论描述"
```
