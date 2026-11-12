# Literature Evidence Matrix — Schema (v1.0)

**Project:** 七大类食品合规缺陷的对比分析 / Comparative analysis of compliance defects across seven food categories (Zhejiang, China)

**Purpose of this file:** 本文件仅定义结构化证据数据库（Literature_Evidence_Matrix）的字段结构、取值集、证据判定规则与工作流程。本文件不包含任何文献内容提取结果。

**Stage status:** Stage 0 — Schema definition only. 21 PDFs have NOT been read at this stage. No Excel, no review text, no evidence entries have been produced.

**Data source boundary:** 全部字段只能来自本地 21 篇 PDF 原文。禁止联网检索、禁止新增文献、禁止凭常识补全。

---

## 0. 源文件清单（已清点，待处理）

| # | 文件夹（Folder/Source Category） | PDF 数量 |
|---|---|---|
| 1 | 中国监管研究 | 12 |
| 2 | 食源性疾病 | 2 |
| 3 | 全球食品安全 | 2 |
| 4 | 监管检查数据 | 3 |
| 5 | HACCP-GMP-ISO | 1 |
| 6 | 风险治理 | 1 |
| | **合计** | **21** |

**已识别的重复文件（处理前需人工确认）：**

`Comp Rev Food Sci Food Safe - 2024 - Ze - Risk factors affecting the food safety risk in food business operations for.pdf`

该文件同时出现在 **食源性疾病 / 全球食品安全 / 风险治理** 三个文件夹中，另有 1 份位于 `监管检查数据` 之外的第 4 处副本。即该文献在 21 个 PDF 路径中被重复存放。

- 处理规则：每篇**唯一文献**只建立一个 Literature ID，矩阵中只出现一行。
- `Folder/Source Category` 字段允许记录多个文件夹路径（用 `;` 分隔），以便保留溯源痕迹。
- 重复关系属于客观文件状态，记录于该行备注，**不作为两条独立证据参与计数**。

---

## 1. 矩阵主键与行结构

- **一行 = 一篇唯一文献**（一个 Literature ID）。
- **一格 = 一个字段**。
- 一篇文献可映射多个 `Manuscript Section`，但**映射必须有明确证据**（见 §5 规则 R7–R9）。
- 长文本字段（Research Objective / Key Findings / Exact Evidence Location / Potentially Citable Statement）允许 1 条记录内含多条要点，用编号列表分隔，**每条要点后必须附证据位置**。

---

## 2. 字段字典（41 字段）

### 2.1 标识类（Identification）

| # | 字段名 | 中文名 | 定义与填写规则 | 缺失时 |
|---|---|---|---|---|
| 1 | `Literature ID` | 文献编号 | 唯一主键。建议格式 `L01`–`L21`（按最终处理顺序编号，不按文件夹编号），建立后不再变更、不复用 | 必填，不得缺失 |
| 2 | `Folder/Source Category` | 来源文件夹 | 该 PDF 实际所在的本地文件夹名。重复文件记录全部路径，用 `;` 分隔 | 必填 |
| 3 | `File Name` | 文件名 | 完整文件名（含扩展名），与磁盘一致 | 必填 |
| 4 | `Authors` | 作者 | 照抄 PDF 中列出的全部作者，保留原文顺序与姓名拼写。超过 6 位作者时全部列出，不使用 "et al." 截断 | Not reported |
| 5 | `Publication Year` | 发表年份 | 期刊/会议出版年。以 PDF 中标注的出版年为准；若有 online-first 年与卷期年不一致，两者都写，格式 `2023 (online) / 2024 (issue)` | Not reported |
| 6 | `Title` | 标题 | 原文标题，逐字照抄（含大小写与标点），不翻译、不改写、不合并 | Not reported |
| 7 | `Journal/Source` | 期刊/来源 | 期刊全名；学位论文写学位授予单位 + 学位类型；标准/法规写标准号或法规全称 | Not reported |
| 8 | `DOI` | DOI | 仅抄录 PDF 中实际出现的 DOI。**严禁根据标题推算、拼接或猜测 DOI**；未出现则填 Not reported | Not reported |
| 9 | `URL` | 链接 | 仅抄录 PDF 中实际出现的 URL（出版社页、数据库页、卷首 URL）。无则 Not reported | Not reported |
| 10 | `Document Type` | 文献类型 | 受控词表，见 §3.1 | Unclear |

### 2.2 研究情境类（Study Context）

| # | 字段名 | 中文名 | 定义与填写规则 | 缺失时 |
|---|---|---|---|---|
| 11 | `Country/Region` | 国家/地区 | 数据来源地/实施地。多国研究全部列出。**只填原文明确的地理范围**，不推断 | Not reported |
| 12 | `Study Population` | 研究对象 | 原文定义的研究主体（人群、企业、批次、产品、样品、检查记录、文献等）。须写清对象类型与纳入标准 | Not reported |
| 13 | `Food Category` | 食品类别 | 原文涉及的具体食品类别，须使用原文术语。**若涉及多个类别，全部列出**，不概括为"食品" | Not reported |
| 14 | `Sample Size` | 样本量 | 原文报告的全部关键样本量及其单位（企业数 / 样品数 / 批次数 / 记录条数 / 纳入文献数 / 访谈数）。**严禁编造**；原文分母不明时写 `Not reported`，不做推算 | Not reported |
| 15 | `Study Period` | 研究时段 | 数据收集或观察的时间范围，原文格式照抄 | Not reported |
| 16 | `Data Source` | 数据来源 | 数据从何而来（监管抽检记录、企业自查、监督检查档案、问卷、访谈、文献二次分析、实验室检测、官方统计等） | Not reported |
| 17 | `Data Type` | 数据类型 | 受控词表，见 §3.2 | Unclear |
| 18 | `Regulatory Inspection Data?` | 是否监管检查数据 | 是 / 否 / Unclear。"是"必须指该数据确为**监管（含政府委托/受监管方执行）的检查或监督记录**，非企业自查或文献综述 | Unclear |
| 19 | `Non-compliance Findings Used?` | 是否使用不符合项 | 是 / 否 / Unclear。"是"指原文把不符合项/违规/缺陷记录作为**分析对象或核心输入** | Unclear |
| 20 | `Enterprise-level Data?` | 是否企业层面数据 | 是 / 否 / Unclear。"是"指可识别或可归属到单个企业/单个生产者的观测 | Unclear |

### 2.3 方法与结果类（Method & Results）

| # | 字段名 | 中文名 | 定义与填写规则 | 缺失时 |
|---|---|---|---|---|
| 21 | `Research Objective` | 研究目的 | 原文自述的研究目标/研究问题。照抄或忠实转述，**不得添加原文没有的目的** | Not reported |
| 22 | `Key Variables` | 关键变量 | 原文实际测量/分析的变量名称与定义（自变量、因变量、控制变量、分类维度等），照抄原文术语 | Not reported |
| 23 | `Original Defect/Hazard Classification` | 原文缺陷/危害分类 | 原文自己建立或采用的缺陷、危害、非符合项分类体系。**必须写原文的分类名称与层级**，不得替换为本文的编码类别 | Not reported |
| 24 | `Potential Correspondence with Our Coding System` | 与本文编码体系的对应关系 | 逐条说明原文分类项与本文编码类别之间是否存在**语义对应**，并说明对应依据。**对应关系只能基于原文分类名称与定义，不得基于推测** | Unclear / Not applicable |
| 25 | `Statistical Methods` | 统计方法 | 原文实际使用的统计/分析方法名称（含软件与版本，若原文报告）。**严禁编造方法**；未报告则 Not reported | Not reported |
| 26 | `Effect Size / Association Measures` | 效应量/关联指标 | 原文报告的效应量与关联指标（OR、RR、χ²、Cramér's V、相关系数、p 值、AUC、贡献率、构成比等）及具体数值。**数值必须逐字照抄** | Not reported |
| 27 | `Risk Assessment Method` | 风险评估方法 | 原文使用的风险评估/评价/分级方法名称与流程（如风险矩阵、危害分析、HACCP 风险分级、熵权-TOPSIS、模糊综合评价、贝叶斯网络等）；无则 Not applicable | Not reported |
| 28 | `Key Findings` | 关键发现 | 原文在 Results/结论中报告的主要发现。**每条发现须能定位到原文位置**。**严禁把 Discussion 中的推测写成 Results**；**严禁把综述文章观点写成原始研究结果** | Not reported |
| 29 | `Limitations` | 局限性 | 原文自述的局限。若原文无局限小节但存在明确的范围限定陈述，可摘录并注明为"原文范围限定陈述"；否则 Not reported | Not reported |

### 2.4 证据映射类（Evidence Mapping）

| # | 字段名 | 中文名 | 定义与填写规则 | 缺失时 |
|---|---|---|---|---|
| 30 | `Evidence Relevant to Our Study` | 与本研究相关的证据内容 | 用本文研究问题（缺陷管理领域集中性 / 类别间差异 / 频率与严重程度关系 / 企业风险画像）的语言，具体写出该文献**能提供哪一条可用证据**。必须落到具体陈述，不得写"整体相关" | — |
| 31 | `Evidence Type` | 证据类型 | 受控词表，见 §3.3。可多选 | Unclear |
| 32 | `Manuscript Section` | 对应论文章节 | 受控词表，见 §3.4。可多选，用 `;` 分隔 | Not directly relevant |
| 33 | `Relationship to Our Study` | 与本研究的关系 | 一句话说明：可作为背景支撑 / 机制解释 / 实证对照 / 方法参照 / 相反证据。**不得因结论一致就自动判为"支持"** | Unclear |
| 34 | `Potentially Citable Statement` | 可引用陈述 | **以本文作者口吻重写的一句话**，可安全放入目标章节。必须满足：只包含该文献原文已写明的内容、不加入因果强化、不加入原文没有的量级。此字段是**改写输出，不是原文引文**；原文措辞需另行保留在 §2.3 字段中 | — |
| 35 | `Supporting Page` | 支持页码 | 提供该证据的 PDF 页码（按 PDF 实际页序，非印刷页码；若印刷页码与 PDF 页序不同，两者都写）。**严禁编造页码** | Not located |
| 36 | `Exact Evidence Location` | 精确证据位置 | 章节标题 / 段落 / 表号 / 图号 / 附录 / 行号级定位，格式建议：`Table 3, p.12, Results 3.2`。**无法定位则填 Not located** | Not located |

### 2.5 溯源与调度类（Traceability & Scheduling）

| # | 字段名 | 中文名 | 定义与填写规则 | 缺失时 |
|---|---|---|---|---|
| 37 | `Relevance to Our Study` | 相关度 | 受控词表，见 §3.5 | Unclear |
| 38 | `Evidence Accessibility` | 证据可获取性 | 受控词表，见 §3.6 | Unclear |
| 39 | `Evidence Traceability` | 证据可溯源性 | 受控词表，见 §3.7 | Unclear |
| 40 | `Citation Priority` | 引用优先级 | 受控词表，见 §3.8 | Not needed |
| 41 | `Theme Tags` | 主题标签 | 从 §4 受控标签表中选取，多个用 `;` 分隔。**标签必须与原文内容一致**，不贴边不贴框 | None |

---

## 3. 受控词表（Controlled Vocabularies）

> 所有枚举值必须逐字使用以下字符串，不得自创近义写法。

### 3.1 `Document Type`（单选）

`Original Research` / `Review` / `Systematic Review` / `Meta-analysis` / `Government/International Report` / `Standard/Guideline` / `Methodological Paper` / `Other`

判定补充：
- 原文自我声明为 "systematic review" → `Systematic Review`，不因有 meta 分析而改判。
- 叙述性综述、文献述评、综述性文章 → `Review`。
- 法规、标准、指南、官方法典（含 CAC/ISO/Codex 文本）→ `Standard/Guideline` 或 `Government/International Report`（以文书性质区分）。
- 无法归类 → `Other`，并在备注写明原因。

### 3.2 `Data Type`（可多选）

`Primary quantitative` / `Primary qualitative` / `Secondary quantitative` / `Secondary qualitative` / `Mixed-methods` / `Literature-based` / `Regulatory/administrative records` / `Laboratory analytical` / `Policy/legal text` / `Not reported` / `Unclear`

### 3.3 `Evidence Type`（可多选）

`Background evidence` / `Mechanism/process evidence` / `Empirical evidence` / `Regulatory evidence` / `Methodological evidence` / `Comparative evidence` / `Contradictory/alternative evidence`

判定补充：
- `Contradictory/alternative evidence` 仅在**原文明确给出与常见结论不同的观点或数据**时使用。
- **不得**因为某文献与本研究结果不一致就强行判为"矛盾证据"，也**不得**自行解释差异产生的原因。

### 3.4 `Manuscript Section`（多选，分隔符 `;`）

`Introduction 1.1` / `Introduction 1.2` / `Introduction 1.3` / `Discussion 4.1` / `Discussion 4.2` / `Discussion 4.3` / `Discussion 4.4` / `Discussion 4.5` / `Methods` / `Results interpretation` / `General background` / `Not directly relevant`

映射对照（章节 → 所需证据类型）：

| Manuscript Section | 目标证据内容 | 允许的 Evidence Type（参考，非强制） |
|---|---|---|
| Introduction 1.1 | 全球食品安全问题、食源性疾病负担、全球供应链复杂性、食品安全风险治理、风险导向与预防性管理 | Background evidence |
| Introduction 1.2 | 食品生产过程控制、HACCP、GMP、GHP、prerequisite programs、ISO 22000、卫生管理、原料控制、生产过程控制、清洁消毒、设备设施、人员卫生、检验与追溯 | Mechanism/process evidence；Background evidence；Standard/Guideline |
| Introduction 1.3 | 食品监督检查、regulatory inspection、inspection findings、inspection non-compliance、risk-based inspection、food safety surveillance、inspection data analysis、中国食品安全监管、食品生产企业合规风险、风险导向监管 | Regulatory evidence；Empirical evidence；Background evidence |
| Discussion 4.1 | 卫生、虫害控制、清洁消毒、原料与仓储、过程控制、食品生产企业日常管理缺陷 | Empirical evidence；Mechanism/process evidence |
| Discussion 4.2 | 不同食品类别风险差异、不同生产工艺导致的控制环节差异 | Comparative evidence；Empirical evidence |
| Discussion 4.3 | 缺陷频率与严重程度、critical/major/minor violations、risk severity、risk prioritization、高频问题与高危问题的区别 | Empirical evidence；Comparative evidence |
| Discussion 4.4 | 企业风险画像、risk profiling、risk scoring、enterprise-level risk classification、cluster analysis、K-means、多维风险特征 | Methodological evidence；Empirical evidence |
| Discussion 4.5 | 监督检查数据局限、检查人员判断、区域代表性、横断面数据、纵向数据、多源监管数据融合 | Empirical evidence；Methodological evidence |
| Methods | 编码体系、统计方法、风险画像方法 | Methodological evidence |
| Results interpretation | 对本研究结果的既有文献对照 | Empirical evidence；Comparative evidence |

### 3.5 `Relevance to Our Study`（单选）

`Direct` / `Moderate` / `Indirect` / `Low`

- `Direct`：研究对象、数据类型或分析层级与本研究高度重合（如同为监管检查不符合项分析、同为企业层面风险分级）。
- `Moderate`：覆盖本研究的一个明确章节议题，但对象或方法有实质差异。
- `Indirect`：仅能提供背景性或机制性支撑。
- `Low`：与本研究无实质关联。

### 3.6 `Evidence Accessibility`（单选）

`Full text` / `Abstract-only analysis` / `Partial text (tables/figures only)` / `Unclear`

- **全文无法读取时必须填 `Abstract-only analysis`**，并在证据提取范围中注明"仅摘要"。
- 摘要分析所得内容**不得写入 `Key Findings` 字段**，只能写入 `Potentially Citable Statement` 并标注"（依据摘要）"。

### 3.7 `Evidence Traceability`（单选）

`Fully traceable` / `Partially traceable` / `Not located`

- `Fully traceable`：字段内容均有页码 + 精确位置可回溯。
- `Partially traceable`：部分字段可回溯，部分仅依据摘要或无法定位。
- `Not located`：无法在原文中定位到支持该记录的具体位置。

### 3.8 `Citation Priority`（单选）

`Core` / `Supporting` / `Supplementary` / `Not needed`

- `Core`：Discussion 核心论断必需，或 Introduction 关键论断的第一顺位来源。
- `Supporting`：直接支撑某章节论断。
- `Supplementary`：背景补充或对照参考。
- `Not needed`：不进入最终引文清单。

---

## 4. 主题标签受控表（`Theme Tags`）

标签仅可从下表选取，不自创：

**宏观背景类**：`Global food safety burden` / `Foodborne disease epidemiology` / `Global food supply chain complexity` / `Food safety governance` / `Risk-based regulation` / `Preventive food safety management`

**生产过程控制类**：`HACCP` / `GMP` / `GHP` / `Prerequisite programs` / `ISO 22000` / `Food safety management system` / `Hygiene management` / `Raw material control` / `Process control` / `Cleaning and disinfection` / `Pest control` / `Equipment and facilities` / `Personnel hygiene` / `Testing and traceability` / `Storage and warehousing`

**监督检查类**：`Regulatory inspection` / `Inspection findings` / `Inspection non-compliance` / `Risk-based inspection` / `Food safety surveillance` / `Inspection data analysis` / `China food safety regulation` / `Enterprise compliance risk` / `Sampling inspection` / `Supervisory inspection`

**风险评价类**：`Risk assessment method` / `Risk severity` / `Risk prioritization` / `Risk scoring` / `Risk profiling` / `Enterprise-level classification` / `Cluster analysis` / `K-means clustering` / `Multidimensional risk characteristics`

**缺陷与危害类**：`Defect frequency` / `Defect severity` / `Critical/major/minor violations` / `Hazard analysis` / `Category-specific risk` / `Process-specific risk`

**方法与数据类**：`Inspection data limitation` / `Inspector judgement` / `Regional representativeness` / `Cross-sectional data` / `Longitudinal data` / `Multi-source data integration` / `Coding scheme` / `Statistical method`

**其他**：`None`

---

## 5. 证据纪律规则（Evidence Discipline Rules）

以下规则优先级高于任何字段的填写便利性。

| 编号 | 规则 |
|---|---|
| R1 | 所有内容必须来自 PDF 原文。禁止联网检索、禁止补充新文献。 |
| R2 | 禁止根据标题推测结论。 |
| R3 | 禁止根据关键词推测结论。 |
| R4 | 禁止根据常识补充作者未写出的内容。 |
| R5 | 禁止把摘要内容扩展为全文结论。 |
| R6 | 禁止把 Discussion 中的推测写成 Results。 |
| R7 | 禁止把综述文章的观点写成原始研究结果。 |
| R8 | 禁止编造数据、样本量、DOI、页码、统计方法。 |
| R9 | 禁止因为结论一致就判为"支持"；禁止因为结论不同就自行解释差异原因。 |
| R10 | 禁止"研究不足"的判断。**尤其不得以"未检索到相关文献"推断"该方向存在研究空白"**。 |
| R11 | 禁止因文献内容丰富就强行映射到多个章节；无明确证据即不映射。 |
| R12 | 原文未说明 → `Not reported`；无法判断 → `Unclear`；无法定位 → `Not located`；全文不可读 → `Abstract-only analysis`。 |

### 5.1 缺失值使用规范

- `Not reported`：原文确无该项信息。
- `Not applicable`：该字段对本文献类型不适用（如 Original Research 无风险评估方法时，填 `Not applicable` 而非 `Not reported`）。
- `Unclear`：原文有相关表述但不足以判定。
- `Not located`：内容存在但无法定位位置。
- **禁止留空单元格，禁止填 `—`、`N/A`、空白、`待补充` 等非受控写法。**

---

## 6. 与本文研究的对应基准（映射参照系）

本矩阵的映射判断以下列**本文既定研究设计**为基准。基准内容不在本阶段论证，仅作为字段判定参照。

- **研究对象**：浙江省食品生产企业监督检查中发现的食品安全不符合项。
- **数据规模**：138 家食品生产企业；1313 条监督检查不符合项；7 个食品类别。
- **核心研究问题**：
  1. 食品生产企业食品安全缺陷主要集中在哪些管理领域？
  2. 不同食品类别的缺陷模式是否存在显著差异？
  3. 缺陷发生频率是否能够反映食品安全风险严重程度？
  4. 能否基于企业层面的缺陷强度、风险覆盖广度和缺陷结构形成不同的企业风险画像？

### 6.1 待用户补充的基准信息（阻塞项）

以下两项在开始批量提取前必须由作者确认，否则字段 24（`Potential Correspondence with Our Coding System`）无法客观填写：

1. **本文 7 类缺陷编码体系的完整类别名称**（当前仅从 Discussion 4.2 提纲中可见：肉制品、乳制品、饮料、食用油、方便食品、特殊膳食食品共 6 类，**第 7 类未提供，不得推测**）。
2. **本文 7 个食品类别的完整名称**（同上，提纲未列全）。
3. 若有：不符合项**严重程度分级**（critical / major / minor）的判定标准与分级变量来源。

> 在作者补充前，字段 24 一律填 `Pending author input`，**不得**由提取者自行拟定映射。

---

## 7. 分批处理计划（21 篇 PDF）

### 7.1 分批原则

1. **按文件夹分批**，便于 Folder/Source Category 字段一致填写。
2. **重复文件集中在同一批次的前段处理**，先完成去重与唯一 ID 确认，后续批次不再重复。
3. **先易后难**：先处理结构清晰、可读性高的文献，以校准字段理解与受控词表；再处理长文、扫描件、纯标准文本。
4. **每批 2–4 篇**，每批结束后立即落盘为独立 CSV/Markdown 增量文件，避免长上下文丢失。
5. **每批结束执行一次自检**（§7.4 校验清单）。

### 7.2 批次安排

| 批次 | 内容 | 篇数 | 批次目的 |
|---|---|---|---|
| Batch 0 | 重复文件识别与唯一 ID 分配（Ze 2024, Comp Rev Food Sci Food Safe） | 1 unique | 去重、ID 体系建立、字段试填模板 |
| Batch 1 | `全球食品安全` 中除重复文件外的条目 + `HACCP-GMP-ISO` | 1–2 | 标准/指南类文档（Document Type = Standard/Guideline）字段校准 |
| Batch 2 | `风险治理` 中除重复文件外的条目 | 0–1 | 治理/监管策略类 |
| Batch 3 | `中国监管研究` 第 1 批 | 3 | 中文期刊文章字段校准（含中文题录信息） |
| Batch 4 | `中国监管研究` 第 2 批 | 3 | 中文实证/评估类 |
| Batch 5 | `中国监管研究` 第 3 批 | 3 | 中文行业/类别特异类（肉制品、食用油、保健食品等） |
| Batch 6 | `中国监管研究` 第 4 批 | 3 | 中文监管与宏观类 |
| Batch 7 | `监管检查数据` | 3 | 英文监管检查数据实证类（本研究最直接的对标文献，优先级最高） |
| Batch 8 | `食源性疾病` 中除重复文件外的条目 | 1 | 疾病负担/流行病学类（Introduction 1.1 支撑） |
| — | 合并去重后唯一文献合计 | 18 unique | （21 个 PDF 路径 − 3 重复副本） |

> 唯一文献数需在 Batch 0 完成后以实际去重结果为准更新；上表"18"为初步估算，**不得作为最终计数写入任何输出文件**。

### 7.3 每批处理的标准步骤

1. 读取 PDF 全文（或确认可读性并标记 `Abstract-only analysis`）。
2. 提取 §2.1–§2.5 全部 41 字段，逐字段记录证据位置。
3. 判定 `Manuscript Section`（可多选，但每项须有明确证据；无证据则不映射）。
4. 判定 `Evidence Accessibility` 与 `Evidence Traceability`。
5. 写出 `Potentially Citable Statement`（本文作者口吻改写，标注依据范围：全文/摘要）。
6. 落盘为增量文件：`Literature_Matrix_BatchN.md`（或 CSV），保存至 `output`。
7. 执行 §7.4 校验清单。

### 7.4 每批自检校验清单

- [ ] 41 个字段全部有值，无空单元格
- [ ] 所有缺失值使用 §5.1 受控写法
- [ ] `Document Type` / `Evidence Type` / `Manuscript Section` / `Relevance` / `Citation Priority` 取值均来自 §3–§4 受控词表
- [ ] 每条 `Key Findings` 均有 `Supporting Page` + `Exact Evidence Location`
- [ ] `Sample Size`、`Effect Size`、`Statistical Methods` 数值逐字核对原文，无编造
- [ ] `Potentially Citable Statement` 中不含原文没有的因果表述或量级
- [ ] `Abstract-only analysis` 文献未向 `Key Findings` 写入内容
- [ ] 综述/系统综述文献未向 `Key Findings` 写入原始研究结果
- [ ] 无文献被判定为"研究空白"依据
- [ ] Literature ID 唯一，无重复行
- [ ] 未联网、未新增文献

---

## 8. 输出文件规范

| 用途 | 文件名 | 保存位置 |
|---|---|---|
| 本 Schema | `Literature_Matrix_Schema.md` | `文献梳理\output` |
| 各批次增量矩阵 | `Literature_Matrix_BatchN.md` / `.csv` | `文献梳理\output` |
| 合并后完整矩阵 | `Literature_Evidence_Matrix.md` / `.xlsx` | `文献梳理\output`（后续阶段，本阶段不生成） |
| 证据缺口与冲突登记 | `Evidence_Gap_Log.md` | `文献梳理\output`（后续阶段，本阶段不生成） |

**本阶段唯一输出文件：** `Literature_Matrix_Schema.md`

---

## 9. 本阶段明确未做的事项

- 未读取任何 PDF
- 未生成 Excel / CSV 矩阵
- 未撰写文献综述
- 未联网检索
- 未新增文献
- 未对任何文献作出相关性、引用优先级或章节映射的实际判定
