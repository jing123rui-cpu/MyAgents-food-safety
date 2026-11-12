# 法规检索（regulation_lookup）

**状态**：已实现 · **阶段**：2 - 法规引用

## 用途

按企业类型和命中检查点，取适用法规条目与条款引用，供报告「法规依据」部分和现场定性使用。

## 引擎实现

| 组件 | 路径 | 职责 |
|---|---|---|
| 加载器 | `audit/script/regulation_loader.py` | 读取注册表与 Markdown 全文 |
| 注册表 | `audit/knowledge/regulations/regulation_registry.yaml` | 12 条法规元数据 |
| 全文 | `audit/knowledge/regulations/REG-*.md` | 条款级内容 |

**类型继承**：`general_food` → `beverage` → `packaged_water`，子类型自动继承父类型法规。例如 `packaged_water` 企业同时适用食品安全法、GB 14881、GB 12695、GB 7101、GB 19298。

## 输入 / 输出

- 输入：`matched_checkpoints`、`enterprise_type`
- 输出：`regulation_references`（法规条目与条款）、`regulation_table`（报告用表格行）

## 法规清单（12 条）

| ID | 名称 | 类型 |
|---|---|---|
| `REG-FOOD-SAFETY-LAW` | 中华人民共和国食品安全法 | 法律 |
| `REG-FOOD-SAFETY-LAW-IMPL` | 食品安全法实施条例 | 行政法规 |
| `REG-FOOD-PRODUCTION-LICENSE` | 食品生产许可管理办法 | 部门规章 |
| `REG-PRODUCTION-LICENSE-REVIEW` | 食品生产许可审查通则 | 规范性文件 |
| `REG-INSPECTION-CHECKLIST` | 食品生产经营监督检查要点表 | 规范性文件 |
| `REG-FOOD-ADDITIVE` | 食品添加剂使用管理规定 | 部门规章 |
| `REG-GB-14881` | GB 14881 食品生产通用卫生规范 | 国家标准 |
| `REG-GB-2760` | GB 2760 食品添加剂使用标准 | 国家标准 |
| `REG-GB-12695` | GB 12695 饮料生产卫生规范 | 国家标准 |
| `REG-GB-7101` | GB 7101 饮料 | 国家标准 |
| `REG-GB-19298` | GB 19298 包装饮用水 | 国家标准 |
| `REG-HACCP` | HACCP 体系通用要求 | 国家标准 |

## 在对话中的用法

1. 确认产品类别 → 确定企业类型（`general_food` / `beverage` / `packaged_water`）。
2. 读 `audit/knowledge/regulations/REG-xxx.md` 取条款原文要点。
3. 引用时写全称 + 条款号，例如 `GB 14881-2013 第 5.1.2 条`。
4. 注册表里没有的法规（如 GB 7718、GB 28050、GB 29921）按训练知识回答，并标注 `【需核对原文】`。

## 局限

- 仅 12 条，标签标识、污染物、致病菌、农药残留等常用标准未入库。
- 无版本追踪与失效提醒，引用前需核实现行有效版本。
- 条款定位依赖 Markdown 全文的写法，不能替代法规数据库。
