# Checkpoint Schema v2.0

---

## 版本说明

```
Schema v1.0 → Schema v2.0
  (Sprint 5 + 5.5)  →  (Sprint 10)
  8 个章节             8 + 8 = 16 个章节
  知识记录模型          自动推理模型
```

**向后兼容**：v2.0 保留 v1.0 全部字段，仅**新增** 8 个章节。所有 v1.0 已编写的 25 个 Checkpoint 无需修改，新建 Checkpoint 必须按 v2.0 完整编写。

---

## Schema 总览

```
Checkpoint Schema v2.0
│
├─ [v1.0 保留]  ① Metadata              标识信息
├─ [v1.0 保留]  ② Inspection Objective  检查目的
├─ [v1.0 保留]  ③ Inspection Method     检查方法
├─ [v1.0 保留]  ④ Required Evidence     证据要求
├─ [v1.0 保留]  ⑤ Common Findings       常见发现项
├─ [v1.0 保留]  ⑥ Risk Level            风险等级
├─ [v1.0 保留]  ⑦ Regulatory References 法规引用
├─ [v1.0 保留]  ⑧ AI Guidance           AI 推理指导
│
├─ [v2.0 新增]  ⑨ Inspection Focus      监管关注重点
├─ [v2.0 新增]  ⑩ Interview             访谈指导
├─ [v2.0 新增]  ⑪ Cross Validation      交叉验证模型
├─ [v2.0 新增]  ⑫ Evidence Chain        证据链
├─ [v2.0 新增]  ⑬ Risk Score            风险评分
├─ [v2.0 新增]  ⑭ AI Action             AI 执行指令
├─ [v2.0 新增]  ⑮ Automation Potential  自动化分级
└─ [v2.0 新增]  ⑯ Dependencies          依赖关系
```

---

## ⑨ Inspection Focus（监管关注重点）

### 字段名称

```yaml
inspection_focus:
  regulatory_concern: "string"       # 监管风险的核心问题
  typical_questions: ["string"]       # 检查员最关心的 3-5 个问题
  red_flags: ["string"]              # 需要立即关注的危险信号
```

### 字段用途

解释"这个检查点真正在防范什么"。不是检查动作的描述，而是监管层面的风险关注点。AI 理解了这个字段，才能在报告中写出有深度的风险分析，而不是机械地罗列"有证书/无证书"。

### 填写规范

- `regulatory_concern`：用一句话说明监管关注的核心。句式："防止……"或"确认……"
- `typical_questions`：检查员在现场会自问的核心问题
- `red_flags`：如果出现即触发关注升级的具体信号

### 示例

```yaml
inspection_focus:
  regulatory_concern: "防止企业从未取得生产许可的供应商处采购食品原料，导致原料安全无法保障"
  typical_questions:
    - "供应商是否具备生产该原料的合法资质？"
    - "许可证是否覆盖了实际采购的全部品种？"
    - "企业是否核验过许可证的真实性？"
    - "许可证过期后企业是否及时停止了采购？"
  red_flags:
    - "供应商许可证品种范围不包含企业采购的原料"
    - "许可证签发机关非企业所在地市场监管部门"
    - "企业提供的许可证复印件无法辨识编号"
```

### AI 如何使用

| 使用场景 | 方式 |
|----------|------|
| 判定时 | AI 将 Findings 与 `red_flags` 比对，命中任意 flag 自动升级风险等级 |
| 报告撰写 | AI 将 `regulatory_concern` 转化为检查结论的背景说明 |
| 问题排序 | AI 按 `red_flags` 的数量和严重程度排列发现项的优先级 |

---

## ⑩ Interview（访谈指导）

### 字段名称

```yaml
interview:
  suggested_interviewees:
    - role: "string"                  # 建议访谈对象（岗位角色）
      priority: "H / M / L"          # 访谈优先级
      reason: "string"               # 为什么访谈该角色
      suggested_questions:
        - question: "string"         # 建议问题
          purpose: "string"          # 通过这个问题想验证什么
          expected_answer: "string"  # 合规情况下的预期回答
```

### 字段用途

为 AI Agent 提供结构化访谈指导。AI 不仅可以查文件、看现场，还应能与企业人员进行对话，通过问答发现文件证据无法覆盖的问题（如人员认知、执行意愿、制度理解等）。

### 填写规范

- `role`：使用企业常见的岗位名称（食品安全总监、采购经理、仓管员、品控员、操作工）
- `priority`：H（必须访谈）/ M（建议访谈）/ L（时间允许时访谈）
- `reason`：解释该角色能提供什么文件证据无法覆盖的信息
- `suggested_questions`：每个问题必须关联 `purpose`，避免随意提问
- `expected_answer`：合规企业的受访者应该能给出的回答，AI 据此判断受访者的认知水平

### 示例

```yaml
interview:
  suggested_interviewees:
    - role: "采购负责人"
      priority: "H"
      reason: "采购负责人最了解供应商审核的实际情况，文件记录可能完善但实际操作可能存在偏差"
      suggested_questions:
        - question: "贵公司如何确保新供应商的资质合规？请描述完整的准入流程。"
          purpose: "验证企业供应商准入流程是否与制度描述一致，评估采购人员对制度的理解程度"
          expected_answer: "收集营业执照和生产许可证→资质审核→样品检测→现场评审（如需）→录入合格名录→审批"
        - question: "如果现有合格供应商的许可证即将到期，贵公司的处理流程是什么？"
          purpose: "评估企业对供应商资质持续合规的管理能力"
          expected_answer: "提前通知供应商续期→到期前索取新证→核验更新→许可证过期未续则暂停该供应商"

    - role: "仓库管理员"
      priority: "M"
      reason: "仓管员最清楚实际入库的原料是否来自合格供应商，以及不合格原料的处理方式"
      suggested_questions:
        - question: "当一批原料到货时，你的验收步骤是什么？"
          purpose: "验证仓管员对验收流程的实际执行情况"
          expected_answer: "核对供应商信息→检查包装完整性→确认生产日期/保质期→通知品控取样→合格后入库"
        - question: "发现包装破损的原料时你怎么处理？"
          purpose: "评估不合格品处理的实际执行"
          expected_answer: "隔离到不合格区→标识→通知品控/采购处理"
```

### AI 如何使用

| 使用场景 | 方式 |
|----------|------|
| 检查中 | AI 按 `role` 选择受访者，按 `suggested_questions` 发起对话 |
| 追问 | 受访者回答与 `expected_answer` 严重不符时，AI 进行追问 |
| 记录 | AI 将访谈结果写入检查记录，作为证据的一部分 |
| 交叉验证 | AI 将访谈结果与文件记录比对，不一致时标记为异常 |

---

## ⑪ Cross Validation（交叉验证模型）

### 字段名称

```yaml
cross_validation:
  data_sources:                        # 需要交叉验证的数据源
    - source: "string"                # 数据源名称
      type: "记录 / 系统 / 人员 / 现场"  # 数据源类型
      content: "string"               # 需要提取的具体数据
      extraction_method: "自动 / 手动"   # 数据提取方式

  validation_rules:                    # 交叉验证规则
    - rule_id: "CV-{编号}"
      description: "string"           # 验证规则描述
      sources: ["数据源A", "数据源B"]   # 参与验证的数据源
      logic: "string"                 # 验证逻辑（A 应等于 B / A 应包含 B / A 不应超过 B）
      severity_if_fail: "H / M / L"   # 验证失败时的严重程度
      alert_condition: "string"       # 触发报警的具体条件
```

### 字段用途

将 Checkpoint 从"单点检查"升级为"多点三角验证"。AI 不再只检查一份文件，而是对比多个来源的信息一致性，发现单点检查无法发现的深层问题（如记录造假、数据矛盾、系统性偏差）。

### 填写规范

- `data_sources`：列出本检查点涉及的全部数据来源，至少 2 个以上才能形成交叉验证
- `extraction_method`：标记"自动"（AI 可直接读取）或"手动"（需人工输入）
- `validation_rules`：每条规则说明比较的内容、比较的逻辑、失败后的严重程度

### 示例

```yaml
cross_validation:
  data_sources:
    - source: "合格供应商名录"
      type: "记录"
      content: "供应商名称、许可证编号、品种范围、有效期"
      extraction_method: "自动（OCR / 文件读取）"
    - source: "进货台账"
      type: "记录"
      content: "原料名称、供应商名称、进货日期"
      extraction_method: "自动（OCR / Excel 读取）"
    - source: "采购合同/订单"
      type: "记录"
      content: "供应商名称、原料名称、采购数量"
      extraction_method: "自动（OCR / 文件读取）"
    - source: "仓库入库记录"
      type: "系统（ERP/WMS）"
      content: "入库单号、供应商、原料、数量、日期"
      extraction_method: "自动（系统对接/截图OCR）"
    - source: "采购负责人访谈"
      type: "人员"
      content: "新供应商准入流程描述"
      extraction_method: "手动（AI 记录）"

  validation_rules:
    - rule_id: "CV-RM-001-01"
      description: "进货台账中的供应商是否都在合格名录中"
      sources: ["进货台账", "合格供应商名录"]
      logic: "进货台账中的供应商名称集合应是合格供应商名录的子集"
      severity_if_fail: "H"
      alert_condition: "进货台账中存在供应商不在合格名录中"

    - rule_id: "CV-RM-001-02"
      description: "采购合同中的供应商与进货台账是否一致"
      sources: ["采购合同/订单", "进货台账"]
      logic: "同一批次的供应商名称在采购合同和进货台账中应完全一致"
      severity_if_fail: "H"
      alert_condition: "合同供应商与台账供应商不一致"

    - rule_id: "CV-RM-001-03"
      description: "仓库入库记录与进货台账是否一致"
      sources: ["仓库入库记录", "进货台账"]
      logic: "同一原料的入库数量与进货台账记录数量之差不应超过合理损耗范围 (≤5%)"
      severity_if_fail: "M"
      alert_condition: "数量差异超过 5% 或入库记录中存在台账中不存在的批次"

    - rule_id: "CV-RM-001-04"
      description: "采购负责人回答与实际文件是否一致"
      sources: ["采购负责人访谈", "合格供应商名录", "进货台账"]
      logic: "采购负责人描述的供应商准入流程应与制度文件一致，新供应商应在合格名录中"
      severity_if_fail: "M"
      alert_condition: "人员回答与文件记录不一致"
```

### AI 如何使用

| 使用场景 | 方式 |
|----------|------|
| 数据采集 | AI 按 `data_sources` 自动读取多源数据 |
| 自动验证 | AI 逐条执行 `validation_rules` 中的逻辑判断 |
| 异常标记 | 验证失败的规则自动标记为发现项，`severity_if_fail` 决定风险级别 |
| 交叉报告 | 在检查报告中生成交叉验证汇总表，展示各数据源的对比结果 |

---

## ⑫ Evidence Chain（证据链）

### 字段名称

```yaml
evidence_chain:
  chain_id: "EC-{编号}"               # 证据链 ID
  chain_name: "string"                # 证据链名称
  description: "string"               # 证据链整体描述

  upstream:                            # 上游依赖
    - checkpoint_id: "string"         # 上游检查点 ID
      relationship: "前置 / 输入 / 条件"  # 关系类型
      data_flow: "string"             # 传递的数据内容

  downstream:                          # 下游影响
    - checkpoint_id: "string"         # 下游检查点 ID
      relationship: "后继 / 输出 / 触发"  # 关系类型
      impact: "string"                # 当前检查点结果对下游的影响

  chain_integrity:
    required_chain: ["CP-..."]        # 必须完整的链条环节
    break_handling: "string"          # 链条断裂时的处理策略
```

### 字段用途

描述检查点之间的数据流和逻辑依赖关系，形成完整的证据链网络。AI 利用证据链进行推理：某个环节的异常会自动触发上下游的联动检查。同时，证据链确保检查的完整性——不会因为"看起来没问题"就跳过前置检查。

### 关系类型

| 关系 | 说明 | 示例 |
|------|------|------|
| `前置` | A 必须在 B 之前执行 | 供应商审核（前置）→ 原料验收 |
| `输入` | A 的输出是 B 的输入数据 | 合格名录（输入）→ 进货查验的供应商比对 |
| `条件` | A 的结果决定 B 是否执行 | 原料验收不合格（条件）→ 不合格隔离检查 |
| `后继` | B 在 A 之后自然执行 | 原料验收（后继）→ 原料入库 |
| `输出` | A 产生 B 需要的数据 | 进货查验记录（输出）→ 追溯检查 |
| `触发` | A 的结果触发 B 的启动 | 发现不合格原料（触发）→ 供应商整改追踪 |

### 示例

```yaml
evidence_chain:
  chain_id: "EC-RM-FULL"
  chain_name: "原料管理全证据链"
  description: "从供应商准入到原料投入生产的完整证据链，覆盖供应商资质审核、合格名录管理、进货查验、贮存管理"

  upstream:
    - checkpoint_id: "CP-BEV-QLF-001"
      relationship: "前置"
      data_flow: "企业生产许可证信息（确认企业有资质生产，才能判定其原料管理合规性）"
    - checkpoint_id: "CP-BEV-RM-003"
      relationship: "前置"
      data_flow: "供应商准入评价结果（新供应商必须完成准入评价才能出现在合格名录中）"

  downstream:
    - checkpoint_id: "CP-BEV-RM-015"
      relationship: "后继"
      impact: "原料入库后的库存管理依赖于验收环节的批次信息完整性"
    - checkpoint_id: "CP-BEV-BCH-007"
      relationship: "输出"
      impact: "投料记录中的原料批号来自进货查验记录，查验记录不完整则投料追溯链断裂"
    - checkpoint_id: "CP-BEV-TBC-003"
      relationship: "输出"
      impact: "追溯测试的原料端数据来自进货查验记录，记录缺失则正向追溯无法完成"
    - checkpoint_id: "CP-BEV-CMP-009"
      relationship: "触发"
      impact: "验收发现不合格原料应触发纠正措施"

  chain_integrity:
    required_chain:
      - "CP-BEV-RM-001"   # 供应商许可证
      - "CP-BEV-RM-003"   # 供应商准入
      - "CP-BEV-RM-005"   # 合格名录
      - "CP-BEV-RM-006"   # 进货查验
      - "CP-BEV-RM-011"   # 不合格隔离
      - "CP-BEV-RM-013"   # 原料贮存
    break_handling: "如果 required_chain 中任一环节被判定为不符合，上游检查点自动标记为待复核，下游检查点降低评级的置信度"
```

### AI 如何使用

| 使用场景 | 方式 |
|----------|------|
| 推理 | AI 按 `upstream` 回溯到前置检查点，看是否有未完成或不合格的环节 |
| 联动 | 当前检查点判定不符合时，AI 自动检查 `downstream` 中的后继检查点是否受影响 |
| 完整性 | AI 检查 `required_chain` 是否全部完成，未完成时发出警告 |
| 优先级 | AI 按证据链顺序安排检查顺序，确保前置依赖先完成 |

---

## ⑬ Risk Score（风险评分）

### 字段名称

```yaml
risk_score:
  base_score: 0-100                            # 基础风险分值
  scoring_criteria:                            # 评分细则
    - condition: "string"                     # 判定条件
      score: 0-100                            # 该条件下的分值
      reasoning: "string"                     # 分值设定理由

  modifiers:                                   # 修正因子
    - factor: "scope"                         # 范围修正
      values:                                 
        systemic: 1.5                         # 系统性问题（整个模块都受影响）
        multiple: 1.2                         # 多批次问题
        isolated: 1.0                         # 孤立问题
    - factor: "repeat"                        # 重复修正
      values:
        first_time: 1.0                       # 首次发现
        repeated: 1.5                         # 同类型问题再次出现
        persistent: 2.0                       # 前次检查已提出仍未整改

  cumulative_impact:                          # 累计影响
    affected_module: "string"                 # 影响到的模块
    module_weight: 0-1                        # 本检查点在该模块中的权重
    cascade_to_downstream: true/false         # 是否级联到下游
```

### 字段用途

将定性风险判定（RISK-01~04）扩展为定量评分（0-100）。支持风险细化排序（同级别内区分严重程度）、企业累计风险计算、风险趋势追踪。

### 评分映射

| RISK Level | 分值范围 | 说明 |
|------------|----------|------|
| RISK-01 | 81-100 | 重大风险，需要立即停产/召回 |
| RISK-02 | 61-80 | 较大风险，限期整改 |
| RISK-03 | 31-60 | 一般风险，制定整改计划 |
| RISK-04 | 0-30 | 轻微风险/观察项 |

### 示例

```yaml
risk_score:
  base_score: 70
  scoring_criteria:
    - condition: "供应商完全无生产许可证"
      score: 95
      reasoning: "无证供应商提供的原料完全无法保障安全，属于最严重的合规问题"
    - condition: "许可证过期仍在采购"
      score: 85
      reasoning: "许可证过期等同于无证，但存在企业疏忽遗忘续期的可能，略低于完全无证"
    - condition: "许可证品种范围不覆盖"
      score: 75
      reasoning: "超范围经营，但该供应商可能持有其他有效的许可证"
    - condition: "许可证信息不一致但有效"
      score: 50
      reasoning: "可能是企业更名、地址变更未及时更新，需进一步核实"
    - condition: "许可证完整且有效"
      score: 10
      reasoning: "基本无风险，仅为常规记录留存"

  modifiers:
    - factor: "scope"
      values:
        systemic: 1.5
        multiple: 1.2
        isolated: 1.0
    - factor: "repeat"
      values:
        first_time: 1.0
        repeated: 1.5
        persistent: 2.0

  cumulative_impact:
    affected_module: "原料管理"
    module_weight: 0.25
    cascade_to_downstream: true
```

### 累计风险计算规则

```
企业累计风险分 = Σ(各检查点得分 × 修正因子) / 检查点总数

单个检查点最终分 = scoring_criteria 匹配分 × scope_modifier × repeat_modifier

企业总体风险等级：
  0-20    → 低风险
  21-40   → 一般风险
  41-60   → 较高风险
  61-80   → 高风险
  81-100  → 极高风险
```

### AI 如何使用

| 使用场景 | 方式 |
|----------|------|
| 自动评分 | AI 匹配 `scoring_criteria` 中的条件，确定基础分 |
| 修正计算 | AI 判断 `scope` 和 `repeat` 因子，计算最终分 |
| 累计计算 | AI 按 `module_weight` 累加模块内所有检查点的评分 |
| 趋势分析 | AI 将多次检查的评分绘制为趋势图，判断企业风险变化 |

---

## ⑭ AI Action（AI 执行指令）

### 字段名称

```yaml
ai_action:
  auto_read:                                  # 自动读取的资料
    - resource: "string"                     # 资料名称/类型
      format: "PDF / Word / Excel / 图片 / 系统 / 视频"  # 格式
      purpose: "string"                      # 读取后用于什么
      extraction: "OCR / 结构化数据 / 元数据 / 全文"  # 提取方式

  auto_compare:                               # 自动比对
    - description: "string"                  # 比对内容
      source_a: "string"                     # 比对源 A
      source_b: "string"                     # 比对源 B
      compare_method: "string"               # 比对方法

  auto_judge:                                 # 自动判定
    - condition: "string"                    # 可自动判定的条件
      confidence: "H / M / L"               # 判定置信度

  human_confirm:                              # 需要人工确认
    - item: "string"                         # 需要人工确认的内容
      reason: "string"                       # 为什么需要人工
```

### 字段用途

这是 AI Agent 的"可执行指令"。不再是给人看的检查规范，而是给 AI 的执行脚本。AI 读到这个字段就知道：该读取什么文件、用什么方式提取、比对哪些数据、哪些可以自己判、哪些必须找人工确认。

### 填写规范

- `auto_read`：列出 AI 可以直接读取和处理的资料。`format` 决定 AI 使用的解析引擎
- `auto_compare`：明确的比对逻辑，AI 无需人工介入即可完成
- `auto_judge`：只有当 AI 判定置信度为 H（高）时可以自动写入检查结论
- `human_confirm`：明确划出 AI 不能触碰的边界，避免 AI 越权判定

### 示例

```yaml
ai_action:
  auto_read:
    - resource: "供应商生产许可证（复印件/扫描件）"
      format: "图片 / PDF"
      purpose: "提取许可证编号、企业名称、品种范围、有效期进行自动核验"
      extraction: "OCR + 结构化数据提取"
    - resource: "合格供应商名录"
      format: "Excel / Word"
      purpose: "提取供应商名单与许可证信息比对，验证是否完整收录"
      extraction: "结构化数据"
    - resource: "进货台账"
      format: "Excel / 系统截图"
      purpose: "提取近3个月的所有进货记录，与合格名录交叉比对"
      extraction: "结构化数据"

  auto_compare:
    - description: "比对许可证品种范围与采购原料是否符合"
      source_a: "许可证OCR提取结果（品种明细）"
      source_b: "采购台账（原料名称）"
      compare_method: "关键词匹配：品种明细 是否包含 采购原料"
    - description: "比对许可证有效期"
      source_a: "许可证OCR提取结果（有效期至）"
      source_b: "当前系统日期"
      compare_method: "日期比较：有效期 ＞ 当前日期"

  auto_judge:
    - condition: "许可证OCR完成、品种覆盖、有效期未过期"
      confidence: "H"
    - condition: "许可证OCR完成但品种明细模糊不清（OCR置信度 < 80%）"
      confidence: "M"
    - condition: "许可证图片质量差，OCR 无法提取关键信息"
      confidence: "L"

  human_confirm:
    - item: "许可证真伪核验"
      reason: "AI 无法访问国家市场监管总局的许可证查询系统，需要人工登录查询或电话核实"
    - item: "供应商名称与营业执照一致性判断"
      reason: "企业更名、集团下属不同法人实体等复杂情况需要人工判断"
```

### AI 如何使用

```yaml
# AI 执行流程（伪代码）
for each ai_action.auto_read:
  resource_data = read(resource, format, extraction)
  store(resource_data)

for each ai_action.auto_compare:
  result = compare(source_a, source_b, compare_method)
  store(result)

if all auto_judge.confidence == "H":
  write_conclusion("auto")      # 自动写入结论
elif any auto_judge.confidence == "M":
  write_conclusion("auto_with_note")  # 自动写入但附带说明
else:
  flag_for_human_review()       # 标记为人工复核
```

---

## ⑮ Automation Potential（自动化分级）

### 字段名称

```yaml
automation_potential:
  level: "FULL / SEMI / MANUAL"           # 整体自动化等级

  breakdown:                                 # 各环节自动化分析
    - step: "string"                       # 检查步骤/环节
      automation: "FULL / SEMI / MANUAL"   # 该环节的自动化程度
      tool_required: "string"              # 需要的自动化工具
      confidence: "H / M / L"             # 自动化判定的可信度

  fallback:                                  # 降级策略
    - condition: "string"                  # 降级触发条件
      fallback_to: "MANUAL / SEMI"         # 降级到的级别
```

### 自动化等级定义

| 等级 | 定义 | AI 角色 | 人工角色 |
|------|------|---------|----------|
| FULL | 完全自动，无需人工介入 | 独立完成检查并输出结论 | 仅审批确认 |
| SEMI | 半自动，AI 执行 + 人工确认关键节点 | 完成数据采集、比对、初步判定 | 确认关键判定、处理边界情况 |
| MANUAL | 必须人工执行 | 提供检查指引和资料清单 | 执行现场检查并输入结果 |

### 示例

```yaml
automation_potential:
  level: "SEMI"

  breakdown:
    - step: "许可证信息提取（OCR 识别许可证编号、有效期、品种范围）"
      automation: "FULL"
      tool_required: "OCR 引擎（支持竖排文字、印章文字识别）"
      confidence: "H"

    - step: "许可证有效期自动比对"
      automation: "FULL"
      tool_required: "日期计算模块"
      confidence: "H"

    - step: "供应商品种覆盖范围比对"
      automation: "FULL"
      tool_required: "关键词匹配引擎"
      confidence: "M"
      note: "品种描述的标准不一致时（如'饮料' vs '果蔬汁饮料'），可能需要人工确认"

    - step: "许可证真伪核验"
      automation: "MANUAL"
      tool_required: "人工登录国家市场监管总局官网查询"
      confidence: "L"

    - step: "现场观察许可证公示情况"
      automation: "MANUAL"
      tool_required: "无"
      confidence: "L"
      note: "需要人工查看许可证是否悬挂在显著位置"

  fallback:
    - condition: "图片质量差，OCR 置信度低于 60%"
      fallback_to: "MANUAL"
    - condition: "品种范围描述模糊，AI 无法判断是否覆盖"
      fallback_to: "SEMI（AI 标记不确定项，人工确认）"
```

### AI 如何使用

```yaml
# AI 自动化调度逻辑
match automation_potential.level:
  "FULL":
    execute_full_auto()          # 全自动，完成后通知人工确认
  "SEMI":
    auto_result = execute_semi_auto()  # 自动执行可自动的步骤
    for item in breakdown where automation == "MANUAL":
      create_task_for_human(item)      # 创建人工任务
    collate_results(auto_result, human_input)  # 合并结果
  "MANUAL":
    create_checklist_for_human()       # 仅提供检查清单
```

---

## ⑯ Dependencies（依赖关系）

### 字段名称

```yaml
dependencies:
  dag_id: "DAG-{编号}"                              # DAG 唯一 ID
  module: "string"                                   # 所属模块

  prerequisites:                                     # 前置依赖
    - checkpoint_id: "string"                       # 依赖的检查点 ID
      type: "MUST_PASS / MUST_EXECUTE / OPTIONAL"    # 依赖类型
      description: "string"                          # 依赖说明
      impact_if_missing: "string"                    # 缺少依赖时的处理

  dependents:                                        # 后继依赖
    - checkpoint_id: "string"                       # 依赖本检查点的下游
      type: "DIRECT / INDIRECT"                     # 依赖类型
      description: "string"                          # 依赖说明

  execution_order:                                   # 执行顺序
    order: 1-100                                    # 排序序号（本模块内）
    parallel_with: ["string"]                       # 可并行执行的检查点
    wait_for: ["string"]                            # 必须等待的检查点
```

### 依赖类型定义

| 类型 | 含义 | 执行规则 |
|------|------|----------|
| MUST_PASS | 前置必须判定为符合 | 前置不符合，本检查点自动跳过并标记为"因前置不合格未执行" |
| MUST_EXECUTE | 前置必须已完成执行（无论结果） | 前置未执行，本检查点不能开始 |
| OPTIONAL | 前置不是必需要求 | 前置未执行也可开始本检查点 |

### 示例

```yaml
dependencies:
  dag_id: "DAG-RM-001"
  module: "原料管理"

  prerequisites:
    - checkpoint_id: "CP-BEV-QLF-001"
      type: "MUST_PASS"
      description: "企业必须持有有效的食品生产许可证，才能证明其有资质从事食品生产"
      impact_if_missing: "企业无有效许可证，原料管理检查的意义降低，整体检查结论受影响"

    - checkpoint_id: "CP-BEV-RM-003"
      type: "MUST_EXECUTE"
      description: "供应商准入评价必须已完成，才能检查供应商许可证的合规性"
      impact_if_missing: "未完成准入评价时，无法确认该供应商是否经过正式审核，需补充评价记录"

    - checkpoint_id: "CP-BEV-RM-009"
      type: "OPTIONAL"
      description: "包装完整性检查与本检查点无直接依赖关系"
      impact_if_missing: "无影响"

  dependents:
    - checkpoint_id: "CP-BEV-RM-005"
      type: "DIRECT"
      description: "许可证审查通过是供应商录入合格名录的前提条件"
    - checkpoint_id: "CP-BEV-RM-006"
      type: "DIRECT"
      description: "进货查验时需核验供应商是否在合格名录中，名录来自前置检查点的输出"

  execution_order:
    order: 2
    parallel_with: ["CP-BEV-RM-002"]
    wait_for: ["CP-BEV-RM-003"]
```

### DAG 完整示例（原料管理模块）

```
执行顺序
  │
  ├─ ① CP-BEV-RM-003  供应商准入评价    ← 起始检查点
  │     │
  │     ├─→ CP-BEV-RM-001  供应商许可证   ← 可并行
  │     └─→ CP-BEV-RM-002  供应商检验报告  ← 可并行
  │           │
  │           ├─→ CP-BEV-RM-005  合格名录   ← 等待前3个完成
  │           │     │
  │           │     └─→ CP-BEV-RM-006  进货查验 ← 等待合格名录
  │           │           │
  │           │           ├─→ CP-BEV-RM-007  合格证明
  │           │           ├─→ CP-BEV-RM-008  感官验收
  │           │           ├─→ CP-BEV-RM-009  包装完整性
  │           │           └─→ CP-BEV-RM-010  保质期核对
  │           │                 │
  │           │                 ├─ 合格 → CP-BEV-RM-013  贮存
  │           │                 └─ 不合格 → CP-BEV-RM-011  不合格隔离
  │           │                                │
  │           │                                └─→ CP-BEV-RM-012  退货/让步
  │           │
  │           └─→ CP-BEV-RM-015  FIFO
  │                 └─→ CP-BEV-RM-016  库存标识
  │                       └─→ CP-BEV-RM-017  离墙离地
  │
  ├─→ CP-BEV-RM-018  冷藏监控           ← 如适用
  ├─→ CP-BEV-RM-019  添加剂专库         ← 如适用
  │
  ├─→ CP-BEV-RM-020  PET瓶坯验收        ← 如适用
  │     └─→ CP-BEV-RM-021  瓶盖密封性
  │           └─→ CP-BEV-RM-022  包材贮存
  │
  └─→ CP-BEV-RM-023  添加剂使用记录     ← 如适用
        ├─→ CP-BEV-RM-024  称量复核
        └─→ CP-BEV-RM-025  GB2760符合性
```

### AI 如何使用

| 使用场景 | 方式 |
|----------|------|
| 自动编排 | AI 读取 `execution_order` 确定检查顺序，`parallel_with` 决定并行分支 |
| 前置检查 | AI 执行前检查 `prerequisites`，MUST_PASS 未通过则跳过并说明原因 |
| 资源调度 | AI 按 DAG 分配多个 Agent 并行执行 `parallel_with` 中的检查点 |
| 影响分析 | 当前检查点判定不符合时，AI 按 `dependents` 通知下游检查点调整预期 |

---

## Schema v2.0 完整结构一览

```yaml
checkpoint:
  # ── v1.0 保留 ──
  # ① Metadata
  id: "string"
  name: "string"
  domain: "string"
  module: "string"
  unit: "string"
  category: "string"
  applicable_products: ["string"]
  risk_level: "RISK-01 ~ 04"
  priority: "P0 ~ P3"
  estimated_time: "string"
  version: "string"
  author: "string"

  # ② Inspection Objective
  inspection_objective:
    purpose: "text"
    key_questions: ["string"]

  # ③ Inspection Method
  inspection_methods:
    - step: int
      method: "string"
      action: "text"

  # ④ Required Evidence
  evidence:
    mandatory: [{}]
    optional: [{}]

  # ⑤ Common Findings
  common_findings:
    - finding: "string"
      severity: "string"

  # ⑥ Risk Level
  risk_level_mapping:
    - condition: "string"
      risk_level: "RISK-0X"

  # ⑦ Regulatory References
  references:
    regulations: [{}]
    standards: [{}]

  # ⑧ AI Guidance
  ai_guidance:
    direct_conclusion_when: [{}]
    need_more_evidence_when: [{}]
    cannot_judge_when: [{}]

  # ── v2.0 新增 ──

  # ⑨ Inspection Focus
  inspection_focus:
    regulatory_concern: "text"
    typical_questions: ["string"]
    red_flags: ["string"]

  # ⑩ Interview
  interview:
    suggested_interviewees:
      - role: "string"
        priority: "H/M/L"
        reason: "text"
        suggested_questions:
          - question: "string"
            purpose: "text"
            expected_answer: "text"

  # ⑪ Cross Validation
  cross_validation:
    data_sources:
      - source: "string"
        type: "string"
        content: "string"
        extraction_method: "自动/手动"
    validation_rules:
      - rule_id: "string"
        description: "text"
        sources: ["string"]
        logic: "text"
        severity_if_fail: "H/M/L"
        alert_condition: "text"

  # ⑫ Evidence Chain
  evidence_chain:
    chain_id: "string"
    upstream: [{}]
    downstream: [{}]
    chain_integrity:
      required_chain: ["string"]
      break_handling: "text"

  # ⑬ Risk Score
  risk_score:
    base_score: 0-100
    scoring_criteria: [{}]
    modifiers: [{}]
    cumulative_impact: {}

  # ⑭ AI Action
  ai_action:
    auto_read: [{}]
    auto_compare: [{}]
    auto_judge: [{}]
    human_confirm: [{}]

  # ⑮ Automation Potential
  automation_potential:
    level: "FULL/SEMI/MANUAL"
    breakdown: [{}]
    fallback: [{}]

  # ⑯ Dependencies
  dependencies:
    dag_id: "string"
    prerequisites: [{}]
    dependents: [{}]
    execution_order: {}
```

---

## Schema v1.0 → v2.0 能力升级对比

| 能力 | v1.0 | v2.0 |
|------|------|------|
| 知识记录 | ✓ 结构化 | ✓ 结构化 |
| AI 推理指导 | ✓ AI Guidance | ✓ AI Guidance + Inspection Focus |
| 证据收集 | ✓ 证据清单 | ✓ 证据清单 + Cross Validation |
| 法规引用 | ✓ 法规引用 | ✓ 法规引用 |
| 风险判定 | ✓ 定性分级 | ✓ 定性分级 + 定量评分 |
| 图片识别 | ✗ | ✓ AI Action（OCR） |
| 文件分析 | ✗ | ✓ AI Action（自动读取） |
| 交叉验证 | ✗ | ✓ Cross Validation |
| 自动报告 | ✗ | ✓ Evidence Chain + Risk Score |
| 多 Agent 协同 | ✗ | ✓ Dependencies（DAG 编排） |
| 现场访谈 | ✗ | ✓ Interview（结构化问答） |
| 自动化调度 | ✗ | ✓ Automation Potential |
| 评分可比性 | 模块内可比 | ✓ 企业间可比（标准化评分） |

---

以上为 **Checkpoint Schema v2.0** 完整设计文档。保持 v1.0 全部字段不变，新增 8 个章节 ⑨~⑯，从知识记录模型升级为 AI 自动推理模型。请审阅确认。
