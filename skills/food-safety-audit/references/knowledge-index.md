# 引擎知识索引

> 本文件由 `scripts/gen_knowledge_index.py` 从 `audit/knowledge/` 自动生成，请勿手改。
> 修改知识库后重新运行生成脚本。

## 1. 概览

| 资产 | 数量 | 路径 |
|---|---|---|
| 检查点 | 45 | `audit/knowledge/checkpoints/` |
| 风险规则 | 45 | `audit/knowledge/risk_rules/` |
| 法规条目 | 12 | `audit/knowledge/regulations/` |
| 分类树子域 | 68 | `audit/knowledge/taxonomy/beverage_knowledge_tree.yaml` |

风险等级分布：高 29 项，中 16 项。

**当前知识库覆盖范围**：饮料（beverage）制造业，原料管理 25 项 + 生产过程管理 20 项。
其他食品类别（食用油、方便食品、特殊膳食等）暂无结构化检查点，需按 `workflows/` 方法论人工推导。

## 2. 检查点总表（按分类）

### 生产过程管理（20 项）

| ID | 检查点 | 风险 | 子类 | 主要依据 |
|---|---|---|---|---|
| `CP-BEV-PP-001` | 工艺参数控制 | 高 | 工艺参数监控 | GB 14881、食品安全法 |
| `CP-BEV-PP-002` | 设备运行确认 | 高 | 工艺参数监控 | GB 14881、食品安全法 |
| `CP-BEV-PP-003` | 在线检查 | 高 | 工艺参数监控 | GB 14881、食品安全法 |
| `CP-BEV-PP-004` | 物料转移 | 中 | 工艺参数监控 | GB 14881、食品安全法 |
| `CP-BEV-PP-005` | 半成品控制 | 高 | 工艺参数监控 | GB 14881、食品安全法 |
| `CP-BEV-PP-006` | 过程监控 | 高 | 工艺参数监控 | GB 14881、食品安全法 |
| `CP-BEV-PP-007` | 时间温度控制 | 高 | 工艺参数监控 | GB 14881、食品安全法 |
| `CP-BEV-PP-008` | 换产管理 | 中 | 工艺参数监控 | GB 14881、食品安全法 |
| `CP-BEV-PP-009` | 生产记录 | 高 | 过程记录 | GB 14881、食品安全法 |
| `CP-BEV-PP-010` | 产品标识 | 中 | 过程记录 | GB 14881、食品安全法 |
| `CP-BEV-PP-011` | 批次管理 | 高 | 过程记录 | GB 14881、食品安全法 |
| `CP-BEV-PP-012` | 关键工序记录 | 高 | 过程记录 | GB 14881、食品安全法 |
| `CP-BEV-PP-013` | 偏差处理 | 高 | 过程偏差处理 | GB 14881、食品安全法 |
| `CP-BEV-PP-014` | 清场 | 中 | 过程偏差处理 | GB 14881、食品安全法 |
| `CP-BEV-PP-015` | 停产恢复 | 高 | 过程偏差处理 | GB 14881、食品安全法 |
| `CP-BEV-PP-016` | 工艺确认 | 高 | 过程验证 | GB 14881、食品安全法 |
| `CP-BEV-PP-017` | 取样控制 | 中 | 过程验证 | GB 14881、食品安全法 |
| `CP-BEV-PP-018` | 过程检验 | 高 | 过程验证 | GB 14881、食品安全法 |
| `CP-BEV-PP-019` | 工艺复核 | 中 | 过程验证 | GB 14881、食品安全法 |
| `CP-BEV-PP-020` | 生产符合性 | 高 | 过程验证 | GB 14881、食品安全法 |

### 原料管理（25 项）

| ID | 检查点 | 风险 | 子类 | 主要依据 |
|---|---|---|---|---|
| `CP-BEV-RM-001` | 供应商生产许可证审查 | 高 | 供应商资质审核 | 食品生产许可管理办法、食品安全法 |
| `CP-BEV-RM-002` | 供应商产品检验报告审查 | 高 | 供应商资质审核 | 食品安全法、GB 14881 |
| `CP-BEV-RM-003` | 供应商准入评价记录检查 | 中 | 供应商评价 | 食品安全法、GB 14881 |
| `CP-BEV-RM-004` | 供应商年度评价记录检查 | 中 | 供应商评价 | GB 14881 |
| `CP-BEV-RM-005` | 合格供应商名录核查 | 高 | 合格供应商名录 | GB 14881、食品安全法 |
| `CP-BEV-RM-006` | 进货查验记录完整性检查 | 高 | 进货查验记录 | 食品安全法、GB 14881 |
| `CP-BEV-RM-007` | 原料合格证明文件核对 | 高 | 进货查验记录 | 食品安全法、GB 14881 |
| `CP-BEV-RM-008` | 原料感官验收执行检查 | 中 | 感官验收 | GB 14881 |
| `CP-BEV-RM-009` | 原料包装完整性检查 | 中 | 感官验收 | GB 14881 |
| `CP-BEV-RM-010` | 原料保质期与生产日期核对 | 高 | 感官验收 | 食品安全法、GB 14881 |
| `CP-BEV-RM-011` | 不合格原料隔离与标识检查 | 高 | 不合格原料处理 | GB 14881 |
| `CP-BEV-RM-012` | 原料退货/让步接收记录检查 | 中 | 不合格原料处理 | GB 14881 |
| `CP-BEV-RM-013` | 原料仓库温湿度控制检查 | 高 | 仓库条件 | GB 14881 |
| `CP-BEV-RM-014` | 原料仓库防虫防鼠设施检查 | 高 | 仓库条件 | GB 14881 |
| `CP-BEV-RM-015` | 原料先进先出执行检查 | 中 | 库存管理 | GB 14881 |
| `CP-BEV-RM-016` | 原料库存标识检查 | 中 | 库存管理 | GB 14881 |
| `CP-BEV-RM-017` | 原料离墙离地存放检查 | 中 | 库存管理 | GB 14881 |
| `CP-BEV-RM-018` | 冷藏原料温度监控检查 | 高 | 特殊原料管理 | GB 14881 |
| `CP-BEV-RM-019` | 食品添加剂专库/专柜检查 | 高 | 特殊原料管理 | GB 14881、食品添加剂管理规定 |
| `CP-BEV-RM-020` | PET瓶坯验收检查 | 中 | 包材验收 | GB 14881 |
| `CP-BEV-RM-021` | 瓶盖密封性检验检查 | 高 | 包材验收 | GB 14881 |
| `CP-BEV-RM-022` | 内包材贮存环境检查 | 中 | 包材贮存 | GB 14881 |
| `CP-BEV-RM-023` | 食品添加剂使用记录检查 | 高 | 添加剂使用记录 | 食品添加剂管理规定、食品安全法 |
| `CP-BEV-RM-024` | 添加剂称量复核检查 | 高 | 添加剂称量复核 | GB 14881 |
| `CP-BEV-RM-025` | 添加剂GB2760符合性抽查 | 高 | GB2760符合性 | GB 2760、食品添加剂管理规定 |

## 3. 检查点 → 风险规则映射

风险规则文件与检查点一一对应，命名规则 `RR-{检查点ID}.yaml`，判定结果三态：`PASS` / `WARNING` / `FAIL`。下表路径相对 `audit/` 目录。

| 检查点 | 风险规则 | 检查点原文 |
|---|---|---|
| `CP-BEV-PP-001` | `RR-CP-BEV-PP-001.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-001.md` |
| `CP-BEV-PP-002` | `RR-CP-BEV-PP-002.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-002.md` |
| `CP-BEV-PP-003` | `RR-CP-BEV-PP-003.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-003.md` |
| `CP-BEV-PP-004` | `RR-CP-BEV-PP-004.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-004.md` |
| `CP-BEV-PP-005` | `RR-CP-BEV-PP-005.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-005.md` |
| `CP-BEV-PP-006` | `RR-CP-BEV-PP-006.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-006.md` |
| `CP-BEV-PP-007` | `RR-CP-BEV-PP-007.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-007.md` |
| `CP-BEV-PP-008` | `RR-CP-BEV-PP-008.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-008.md` |
| `CP-BEV-PP-009` | `RR-CP-BEV-PP-009.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-009.md` |
| `CP-BEV-PP-010` | `RR-CP-BEV-PP-010.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-010.md` |
| `CP-BEV-PP-011` | `RR-CP-BEV-PP-011.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-011.md` |
| `CP-BEV-PP-012` | `RR-CP-BEV-PP-012.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-012.md` |
| `CP-BEV-PP-013` | `RR-CP-BEV-PP-013.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-013.md` |
| `CP-BEV-PP-014` | `RR-CP-BEV-PP-014.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-014.md` |
| `CP-BEV-PP-015` | `RR-CP-BEV-PP-015.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-015.md` |
| `CP-BEV-PP-016` | `RR-CP-BEV-PP-016.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-016.md` |
| `CP-BEV-PP-017` | `RR-CP-BEV-PP-017.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-017.md` |
| `CP-BEV-PP-018` | `RR-CP-BEV-PP-018.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-018.md` |
| `CP-BEV-PP-019` | `RR-CP-BEV-PP-019.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-019.md` |
| `CP-BEV-PP-020` | `RR-CP-BEV-PP-020.yaml` | `knowledge/checkpoints/beverage/production_process/CP-BEV-PP-020.md` |
| `CP-BEV-RM-001` | `RR-CP-BEV-RM-001.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-001.md` |
| `CP-BEV-RM-002` | `RR-CP-BEV-RM-002.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-002.md` |
| `CP-BEV-RM-003` | `RR-CP-BEV-RM-003.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-003.md` |
| `CP-BEV-RM-004` | `RR-CP-BEV-RM-004.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-004.md` |
| `CP-BEV-RM-005` | `RR-CP-BEV-RM-005.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-005.md` |
| `CP-BEV-RM-006` | `RR-CP-BEV-RM-006.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-006.md` |
| `CP-BEV-RM-007` | `RR-CP-BEV-RM-007.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-007.md` |
| `CP-BEV-RM-008` | `RR-CP-BEV-RM-008.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-008.md` |
| `CP-BEV-RM-009` | `RR-CP-BEV-RM-009.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-009.md` |
| `CP-BEV-RM-010` | `RR-CP-BEV-RM-010.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-010.md` |
| `CP-BEV-RM-011` | `RR-CP-BEV-RM-011.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-011.md` |
| `CP-BEV-RM-012` | `RR-CP-BEV-RM-012.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-012.md` |
| `CP-BEV-RM-013` | `RR-CP-BEV-RM-013.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-013.md` |
| `CP-BEV-RM-014` | `RR-CP-BEV-RM-014.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-014.md` |
| `CP-BEV-RM-015` | `RR-CP-BEV-RM-015.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-015.md` |
| `CP-BEV-RM-016` | `RR-CP-BEV-RM-016.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-016.md` |
| `CP-BEV-RM-017` | `RR-CP-BEV-RM-017.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-017.md` |
| `CP-BEV-RM-018` | `RR-CP-BEV-RM-018.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-018.md` |
| `CP-BEV-RM-019` | `RR-CP-BEV-RM-019.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-019.md` |
| `CP-BEV-RM-020` | `RR-CP-BEV-RM-020.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-020.md` |
| `CP-BEV-RM-021` | `RR-CP-BEV-RM-021.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-021.md` |
| `CP-BEV-RM-022` | `RR-CP-BEV-RM-022.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-022.md` |
| `CP-BEV-RM-023` | `RR-CP-BEV-RM-023.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-023.md` |
| `CP-BEV-RM-024` | `RR-CP-BEV-RM-024.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-024.md` |
| `CP-BEV-RM-025` | `RR-CP-BEV-RM-025.yaml` | `knowledge/checkpoints/beverage/raw_material/CP-BEV-RM-025.md` |

## 4. 法规清单

| ID | 名称 | 类型 | 施行/修订 | 适用企业类型 |
|---|---|---|---|---|
| `REG-FOOD-SAFETY-LAW` | 中华人民共和国食品安全法 | 法律 | 2021-04-29 | general_food |
| `REG-FOOD-SAFETY-LAW-IMPL` | 中华人民共和国食品安全法实施条例 | 行政法规/规章 | 2019-10-11 | general_food |
| `REG-FOOD-PRODUCTION-LICENSE` | 食品生产许可管理办法 | 行政法规/规章 | 2020-01-02 | general_food |
| `REG-PRODUCTION-LICENSE-REVIEW` | 食品生产许可审查通则 | 行政法规/规章 | 2022-10-21 | general_food |
| `REG-INSPECTION-CHECKLIST` | 食品生产经营监督检查要点表 | 规范性文件 | 2022-03-15 | general_food |
| `REG-GB-14881` | 食品安全国家标准 食品生产通用卫生规范 | 国家标准 | 2013-11-29 | general_food |
| `REG-GB-12695` | 食品安全国家标准 饮料生产卫生规范 | 国家标准 | 2016-12-23 | beverage |
| `REG-GB-7101` | 食品安全国家标准 饮料 | 国家标准 | 2022-07-28 | beverage |
| `REG-GB-19298` | 食品安全国家标准 包装饮用水 | 国家标准 | 2014-12-24 | packaged_water |
| `REG-HACCP` | HACCP体系 — 危害分析与关键控制点 | 国家标准 | 2021-03-09 | general_food |
| `REG-GB-2760` | 食品安全国家标准 食品添加剂使用标准 | 国家标准 | 2024-02-08 | general_food |
| `REG-FOOD-ADDITIVE` | 食品添加剂使用管理规定 | 行政法规/规章 | 2017-11-07 | general_food |

适用类型为继承关系：`general_food` → `beverage` → `packaged_water`，子类型自动继承父类型法规。

## 5. 分类树（有检查点的域）

### 原料管理（`raw_material_management`，25 项）

| 子域 | 类别 | 检查点 |
|---|---|---|
| 供应商管理 | 供应商资质审核、供应商评价、合格供应商名录 | `CP-BEV-RM-001`、`CP-BEV-RM-002`、`CP-BEV-RM-003`、`CP-BEV-RM-004`、`CP-BEV-RM-005` |
| 原料验收 | 进货查验记录、感官验收、不合格原料处理 | `CP-BEV-RM-006`、`CP-BEV-RM-007`、`CP-BEV-RM-008`、`CP-BEV-RM-009`、`CP-BEV-RM-010`、`CP-BEV-RM-011`、`CP-BEV-RM-012` |
| 原料贮存 | 仓库条件、库存管理、特殊原料管理 | `CP-BEV-RM-013`、`CP-BEV-RM-014`、`CP-BEV-RM-015`、`CP-BEV-RM-016`、`CP-BEV-RM-017`、`CP-BEV-RM-018`、`CP-BEV-RM-019` |
| 包装材料管理 | 包材验收、包材贮存 | `CP-BEV-RM-020`、`CP-BEV-RM-021`、`CP-BEV-RM-022` |
| 食品添加剂管理 | 添加剂使用记录、添加剂称量复核、GB2760符合性 | `CP-BEV-RM-023`、`CP-BEV-RM-024`、`CP-BEV-RM-025` |

### 生产过程管理（`production_process_management`，20 项）

| 子域 | 类别 | 检查点 |
|---|---|---|
| 生产过程控制 | 工艺参数监控、过程记录、过程偏差处理、过程验证 | `CP-BEV-PP-001`、`CP-BEV-PP-002`、`CP-BEV-PP-003`、`CP-BEV-PP-004`、`CP-BEV-PP-005`、`CP-BEV-PP-006`、`CP-BEV-PP-007`、`CP-BEV-PP-008`、`CP-BEV-PP-009`、`CP-BEV-PP-010`、`CP-BEV-PP-011`、`CP-BEV-PP-012`、`CP-BEV-PP-013`、`CP-BEV-PP-014`、`CP-BEV-PP-015`、`CP-BEV-PP-016`、`CP-BEV-PP-017`、`CP-BEV-PP-018`、`CP-BEV-PP-019`、`CP-BEV-PP-020` |
| 关键控制点管理 | CCP识别、关键限值、监控程序、纠偏程序、CCP验证 | - |
| 生产环境管理 | 清洁标准、环境监控、设施卫生、卫生区域管理 | - |
| 交叉污染控制 | 过敏原管理、物理隔离、清洁方案、废弃物处理 | - |
| 产品追溯 | 批次编码、追溯系统、模拟召回、分销记录 | - |
| 返工管理 | 返工授权、返工过程控制、返工记录、返工验证 | - |
| 产品放行 | 放行标准、放行授权、扣留放行、放行文件 | - |

### 已定义但暂无检查点的域

生产过程（`production_process`）、设施设备（`facility_and_equipment`）、人员卫生（`personnel_hygiene`）、清洗消毒（`cleaning_and_sanitation`）、虫害控制（`pest_control`）、仓储物流（`warehousing`）、追溯体系（`traceability`）、HACCP体系（`haccp`）、关键控制点（`ccp`）、良好操作规范（`gmp`）、实验室（`laboratory`）、食品防护（`food_defense`）、食品欺诈预防（`food_fraud_prevention`）、管理体系（`management_system`）、法规合规（`regulatory_compliance`）

这些域是知识库的扩展位置；在补齐检查点前，涉及这些主题时按 `workflows/` 与法规原文人工分析。

## 6. 检索顺序

1. 先在本索引按关键词定位检查点 ID（如「供应商许可证」→ `CP-BEV-RM-001`）。
2. 读 `audit/knowledge/checkpoints/.../{ID}.md` 取检查目的、方法、证据要求、常见发现项、AI 指导。
3. 读 `audit/knowledge/risk_rules/.../RR-{ID}.yaml` 取判定逻辑与风险等级。
4. 读 `audit/knowledge/regulations/{REG-ID}.md` 取条款细节。
5. 需要批量/过滤检索时用 CLI：

```bash
cd audit
python main.py inspect --query supplier      # 用英文关键词，避免 Windows 中文参数转码
python main.py inspect --id CP-BEV-RM-001
python main.py inspect --risk High
```

详见 `references/audit-cli.md`。
