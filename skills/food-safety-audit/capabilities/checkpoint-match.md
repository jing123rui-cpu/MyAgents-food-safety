# 检查点匹配（checkpoint_match）

**状态**：已实现 · **阶段**：1 - 发现项分析

## 用途

把检查员用自然语言写的现场发现（如「供应商许可证已过期」「杀菌温度记录缺失」）映射到结构化检查点 ID，使后续法规检索与规则判定有明确对象。

## 引擎实现

| 组件 | 路径 | 职责 |
|---|---|---|
| 检索器 | `audit/script/search.py` | 关键词匹配、分类过滤 |
| 流水线 | `audit/script/workflow.py`（`InspectionWorkflow.build_context`） | 组织匹配上下文 |
| 注册表 | `audit/knowledge/registry/*.yaml` | 检查点标题、关键词、证据要求 |
| 分类树 | `audit/knowledge/taxonomy/beverage_knowledge_tree.yaml` | 按域/子域过滤适用范围 |

匹配为**确定性文本匹配**（2 字滑窗 + 关键词），不调用大模型。

## 输入 / 输出

- 输入：`findings`（发现项文本列表）、`enterprise_type`（企业类别，用于过滤适用检查点）
- 输出：`matched_checkpoints`（检查点及匹配度）、`unmatched_findings`（未匹配项）

## 在对话中的用法

用户描述现场问题时：

1. 先按 `references/knowledge-index.md` 或 CLI 找候选检查点：
   ```bash
   cd audit
   python main.py inspect --query 供应商许可证
   ```
2. 给出 `CP-BEV-xxx` 后，读对应检查点原文，把用户描述对齐到「检查方法」与「常见发现项」。
3. 无法匹配时明确说明「知识库无对应检查点」，再按 `workflows/` 方法论分析，不要硬套。

## 局限

- 纯文本匹配，同义词/语义改写会漏（如「供货方资质」可能匹配不到「供应商许可证」）。
- 只在已建检查点的域内有效；原料与生产过程以外的主题（人员卫生、清洗消毒、追溯等）暂无检查点。
- 未匹配不等于不违规，只说明知识库未覆盖。
