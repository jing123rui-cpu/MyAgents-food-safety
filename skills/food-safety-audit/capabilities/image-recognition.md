# 图像识别（image_recognition）

**状态**：规划中（无实现） · **阶段**：未接入

## 用途（规划）

从现场照片、证照扫描件、记录拍照中提取文字与场景标签，辅助证据归档与自动比对。

## 现状

| 项 | 状态 |
|---|---|
| 引擎实现 | 无 |
| OCR 库 | 未配置 |
| 图像分类 | 未配置 |
| 与检查流程集成 | 未设计 |

`audit/skills/image_recognition/skill.yaml` 中 `status: planning`，`engine: (none)`。

## 因此当前如何处理图片

1. **不要假装能识别**。收到照片时先说明「本环境无图像识别能力，以下基于你提供的文字描述」。
2. 让用户用文字补充关键信息：证照编号、有效期、品种范围、记录日期、仪表读数、现场状态。
3. 如用户提供的是可读文本截图之外的文件，可请求导出为文字或表格。
4. 需要结构化归档时，按 [检查点匹配](checkpoint-match.md) 把描述映射到检查点，证据类型按检查点「④ Required Evidence」标注（文件扫描 / 记录拍照 / 现场照片）。

## 规划中的输出定义

- `recognised_text`：OCR 提取文本
- `classified_labels`：检测到的对象或状态标签

## 若后续实现，接入点

- 证据采集：`audit/script/evidence.py`
- 上下文组装：`audit/script/ai/context_engine.py`
- 报告附件：`audit/script/ai/report_exporter.py`
