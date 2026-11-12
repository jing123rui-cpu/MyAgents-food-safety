# 检查编排（inspection_review）

**状态**：已实现 · **阶段**：1-3 编排

## 用途

把知识检索、上下文组装、提示词生成、AI 调用串成一次完整检查流程。是其他能力的总调度。

## 引擎实现

| 组件 | 路径 | 职责 |
|---|---|---|
| 流水线 | `audit/script/agent.py`（`InspectionPipeline`） | 统一 `run()` 入口 |
| 工作流 | `audit/script/workflow.py` | 检索与富化 |
| 上下文 | `audit/script/ai/context_engine.py` | 汇总为结构化上下文 |
| 提示词 | `audit/script/ai/prompts.py`（`PromptEngine`） | 模板转提示词 |
| AI 提供方 | `audit/script/ai/deepseek.py` | LLM 调用（可选） |

## 四步流程

```
1. InspectionWorkflow.build_context()      检索检查点 + 注册表 + 法规 + 风险规则
2. ContextEngine.build_context()           汇总、裁剪、格式化
3. PromptEngine.build_inspection_prompt()  模板 → 提示词
4. AIProvider.chat()                       调用 LLM（未配置则走离线模式）
```

## 输入 / 输出

- 输入：`InspectionRequest`（查询条件 + 证据）、`KnowledgeRepository`（已加载知识库）
- 输出：`InspectionContext`（富化上下文）、`AIInspectionResult`（提示词、回答、耗时、提供方信息）

## 在对话中的用法

- 需要**一次拿到某个主题的全部结构化信息**时，用 CLI 的 `inspect` 等价能力：
  ```bash
  cd audit
  python main.py inspect --query 原料验收 --risk High
  ```
  它会同时输出检查点、类别、风险等级、证据要求、法规与对应规则。
- 需要**生成带 AI 分析的完整结果**时，才配置 `DEEPSEEK_API_KEY` 并运行演示脚本：
  ```bash
  export DEEPSEEK_API_KEY=...
  python demo_inspection_ai.py
  ```
- 未配置 API 时不要声称调用了 AI；说明「离线模式，规则与检索结果可用」。

## 局限

- AI 输出质量依赖提示词与模型，需人工校对。
- 流水线没有状态持久化，每次运行独立。
- 演示脚本会写文件，执行前先说明输出位置。
