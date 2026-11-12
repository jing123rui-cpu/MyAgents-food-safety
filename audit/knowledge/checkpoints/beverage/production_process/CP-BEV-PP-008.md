# CP-BEV-PP-008：换产管理

## ① Metadata

```yaml
checkpoint_id: CP-BEV-PP-008
checkpoint_name: 换产管理
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

确认产品切换（换产）操作按规定流程执行，包括生产线清场、设备清洗、物料更换、首件检验等，防止交叉污染和产品混批。

## ③ Applicable Product

全部饮料品类。适用于同一生产线不同产品/规格切换的生产操作。

## ④ Inspection Method

| 步骤 | 方法 | 操作描述 |
|------|------|----------|
| 1 | 文件核查 | 调取换产作业指导书或标准操作程序 |
| 2 | 记录核查 | 从最近一个月记录中选取 3 次换产记录，核对操作步骤 |
| 3 | 现场观察 | 如正在换产，观察操作是否按步骤执行 |
| 4 | 记录核查 | 检查换产后首件检验记录 |
| 5 | 询问 | 询问操作人员不同产品换产时的关键控制点 |

## ⑤ Required Evidence

| 证据 | 类型 | 是否必须 | 说明 |
|------|------|----------|------|
| 换产作业指导书 | 文件扫描 | 必须 | 含换产步骤和检查项目 |
| 换产记录（3次） | 记录拍照 | 必须 | 显示清洁、确认、签字 |
| 首件检验记录 | 文件扫描 | 可选 | 换产后的首件确认 |

## ⑥ Common Findings

| 发现项 | 严重程度 | 说明 |
|--------|----------|------|
| 换产无书面作业指导书 | 较大 | 操作人员凭经验操作 |
| 换产记录缺失或未填写 | 较大 | 换产操作无据可查 |
| 换产清洁不彻底导致残留 | 重大 | 上一产品残留物进入下一产品 |
| 换产未做首件检验即批量生产 | 较大 | 未确认首批产品合格即继续生产 |
| 换产记录与实际操作不符 | 较大 | 记录显示已清洁但现场发现残留 |

## ⑦ Risk Level

| 条件 | 风险等级 |
|------|----------|
| 清洁不彻底导致交叉污染 | RISK-01 重大风险 |
| 无换产指导书或未做首件检验 | RISK-02 较大风险 |
| 换产记录不完整但无实际质量问题 | RISK-03 一般风险 |
| 换产流程规范、记录完整 | RISK-04 轻微风险 |

## ⑧ Regulatory Reference

- `REG-GB-14881` 条款号（产品切换管理要求）
- `REG-FOOD-SAFETY-LAW` 条款号（生产过程控制要求）

## ⑨ AI Guidance

| 场景 | 判定逻辑 | 操作 |
|------|----------|------|
| 换产记录完整且首件检验合格 | 换产管理合规 | 记录为符合 |
| 记录显示清场但现场发现上一产品残留物 | 记录与实际不符 | 扩大检查其他换产记录判断是否为系统性问题 |
| 无换产作业指导书但有培训记录 | 文件缺失 | 视为程序文件缺陷，要求限期制定 |
| 首件检验结果异常但已做调整 | 过程受控可接受 | 确认调整后的验证结果是否合格 |

## ⑩ Output Template

```yaml
checkpoint_result:
  id: CP-BEV-PP-008
  status: "OK / NOK / PENDING"
  findings:
    - finding_id: "FIND-PP-008-01"
      description: "切换产品 | 清场确认 | 首件检验 | 记录完整性 | 判定"
      severity: "high / moderate / minor"
  evidence_collected:
    - evidence_id: "EVID-PP-008-001"
      type: "记录拍照"
      description: "XX次换产操作记录"
  risk_level: "RISK-0X"
  conclusion: "换产管理结论描述"
```
