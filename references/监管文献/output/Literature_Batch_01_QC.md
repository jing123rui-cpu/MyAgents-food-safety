# Literature Batch 01 — QC Report

**Batch:** 01
**Scope:** 本批次仅分析 3 个文件夹中的 5 篇 PDF（HACCP-GMP-ISO、风险治理、监管检查数据）。
**分析目标：** 客观记录每篇文献研究了什么。不是寻找支持证据，不是写综述，不判断研究设计是否正确。
**输出文件：** `Literature_Batch_01.xlsx`（Sheet 1: Literature Matrix；Sheet 2: Evidence Details）
**Schema 依据：** `output\Literature_Matrix_Schema.md` v1.0
**生成日期：** 2026-09-30

---

## 1. 完成情况汇总

| 指标 | 数值 |
|---|---|
| 本批次计划处理 PDF | 5 |
| 实际处理 PDF | 5 |
| 成功读取全文（Full text） | 5 |
| Abstract-only | 0 |
| 全文不可读 | 0 |
| 存在问题的文献 | 0（另有 5 条需注意事项，见 §5） |
| Literature Matrix 行数 | 5（L001–L005） |
| Literature Matrix 字段数 | 34 |
| Evidence Details 行数 | 59 |
| 空单元格 | 0 |
| 联网检索次数 | 0 |
| 新增文献数 | 0 |

### 文件清单与编号

| Literature ID | 文件夹 | 文件名（截断） | 页数 | 字符数（提取） | 全文可读性 |
|---|---|---|---|---|---|
| L001 | HACCP-GMP-ISO | Advancing HACCP QMS and FSMS… systematic review.pdf | 43 | 172,642 | Full text（11 页表格为旋转文本，已通过页面重旋转恢复） |
| L002 | 风险治理 | Comp Rev Food Sci Food Safe - 2024 - Ze - Risk factors…pdf | 20 | 98,716 | Full text |
| L003 | 监管检查数据 | Health Prom J of Aust - 2015 - Brough - Inside the black box…pdf | 5 | 25,344 | Full text |
| L004 | 监管检查数据 | 1-s2.0-S0956713524004274-main.pdf | 9 | 62,449 | Full text |
| L005 | 监管检查数据 | s41598-022-08204-1.pdf | 10 | 51,434 | Full text |

提取工具：pdfplumber 0.11.10。所有页面均返回非空文本层，无扫描件、无空页、无提取错误。

---

## 2. 受控词表使用情况

### 2.1 Document Type（5/5 已填）

| 取值 | 文献 |
|---|---|
| Systematic Review | L001, L002 |
| Original Research | L003, L004, L005 |
| Review / Meta-analysis / Government Report / Standard / Methodological / Other | 无 |

判定依据：L001 标题与正文自述 systematic review，报告 PRISMA 2020 流程图（Figure 1: Identification 640 / Deduplication 630 / Screening 291 / Eligibility 147 / Included 144），并明确声明 meta-analysis 不可行。L002 自述 systematic review，遵循 EFSA 系统综述方法学指南，采用三级筛选与 5% 抽样 inter-rater 一致性检验（77.4%）。二者均未做 meta 分析，因此未归入 `Meta-analysis`。

### 2.2 三个 Yes/No/Unclear 判定

| Literature ID | Regulatory Inspection Data? | Non-compliance Findings Used? | Enterprise-level Data? |
|---|---|---|---|
| L001 | No | No | Unclear |
| L002 | No | No | No |
| L003 | Yes | Yes | Yes |
| L004 | Yes | Yes | Yes |
| L005 | Yes | Yes | Yes |

判定说明（重要，避免误读）：

- **L001 / L002 的 No 指的是「该文献自身使用的数据」**，不是「文献讨论的内容」。
  - L001 的分析单元是 144 篇出版物，不是检查记录；正文中出现的 "noncompliance incidents (44 to 46%)" 是从被纳入的原始研究中摘录的数值（Evidence L001-E04），不构成本综述的非符合项数据。
  - L002 的分析单元是 53 篇文献 + 各国风险评分方法；它**讨论**检查结果作为风险指标（3.5.1 节），但没有把检查记录作为数据使用。
  - L002 的 `Enterprise-level Data?` = No，但需注意：被纳入的 A1 研究大多是场所/企业层面的（37/44 为餐饮场所），这属于「底层文献的层级」，不是本综述数据的层级。已在 Extraction Notes 中注明。
  - L001 的 `Enterprise-level Data?` 记为 Unclear：该综述在 Table 1–6 中记录了个别以工厂/企业为实施单元的干预（例如 milk processing、Thai GMP-HACCP 案例），但综述本身不提供企业层面的聚合数据结构，无法判定。

- **L003 的 Yes 指用于取样而非分析**：29 条非合规通知记录仅用于构建样本框（依 Right to Information Act 2009 取得），研究数据是访谈转录文本。这一点在 Evidence L003-E01 中已标注。

### 2.3 Evidence Type 分布（Evidence Details 共 59 条）

| Evidence Type | 条数 |
|---|---|
| Empirical evidence | 29 |
| Methodological evidence | 10 |
| Background evidence | 6 |
| Regulatory evidence | 6 |
| Mechanism/process evidence | 6 |
| Contradictory/alternative evidence | 2 |

Evidence Type 分布按 Evidence Details 的逐条判定，与 Schema §3.3 受控词表一致，无自创取值。

### 2.4 Relationship to Other Included Studies

5 篇全部填 `Not assessed`。

理由：本批次只做「客观记录每篇研究了什么」，尚未进行任何跨文献结论比较，也未建立批次间的比较基准。按用户指定的取值集，`Not assessed` 是当前唯一诚实的取值。**不得**在后续批次中回填为 `Consistent with other included studies` 之类，除非同时记录比较所依据的具体文献与具体结果。

---

## 3. 缺失值使用情况

按 Schema §5.1，全部缺失值使用受控写法。无空单元格，无 `—` / `N/A` / `待补充` 等非受控写法。

| 缺失类型 | 出现位置 | 数量 |
|---|---|---|
| `Not reported` | L001 Limitations（正文无本综述自身的局限章节）、L001/L003/L005 Study Strengths、L003 Key Variables、L002/L001 若干处 | 见单元格 |
| `Not explicitly stated` | L001/L002/L003 Research Questions | 3 |
| `Not applicable` | 本批次未使用 | 0 |

### 3.1 三处需要特别注意的 Not reported

1. **L001 Limitations = Not reported**。L001 没有任何针对「本综述自身局限」的章节。Section 3.11 的批判性讨论（PDF p.35）针对的是**领域结构性弱点和被纳入研究的弱点**，不是本综述的局限。因此不能把 3.11 的内容抄进 Limitations 字段。已改为在 Limitations 字段中列出可核实的范围性陈述（未预注册 PROSPERO、仅英文文献、多数排除 2018 年前文献），并明确标注这些是范围陈述而非作者自述的局限。
2. **L001 / L003 / L005 Study Strengths = Not reported**。三篇均无 strengths 章节。
   - L002 与 L004 填了内容，但均已标注为「作者自述」并附精确位置（L002 Section 4.1 "Innovations"；L004 Section 4 关于数据覆盖范围的表述）。这两处作者确实主动提出了方法特征，但**不是**正式的 strengths 章节，已在字段内注明。
3. **L003 Key Variables = Not reported**。定性研究未定义分析变量。填写 `Not reported` 而非 `Not applicable`，因为该字段规定缺失时填 Not reported。

---

## 4. 关键数值与页码核对记录

所有 Sample Size、Quantitative Findings、页码均逐条回原文核对。以下为高风险数值的核对结果。

### 4.1 Sample Size 核对

| ID | 记录值 | 原文位置 | 核对 |
|---|---|---|---|
| L001 | 291 screened / 144 included | PDF p.6, Section 2.4 | 一致。Figure 1 标签交叉核对：Screening 291、Included 144 |
| L002 | 53 relevant（44 A1 + 13 A2，4 重叠）；615 条进入筛选 | PDF p.4, Section 3.1 | 一致。注意：564 (Scopus) + 357 (WoS) = 921，去重后 610，+5 snowballing = 615 |
| L003 | 29 名食品经营者 / 29 次访谈 | PDF p.2, Method | 一致 |
| L004 | 86,223 次检查 / 39,838 家 establishments | PDF p.2, Section 2.1；p.3, Table 1 | 一致。Table 1 各类型求和：36,327 + 32,582 + 10,164 + 6,189 + 961 = 86,223 ✓ |
| L005 | 757 家 / 5,550 次检查 / 4,004 次 pre-planned | PDF pp.2-3, Table 1 | 一致。各类型求和：283+332+126+16 = 757 ✓；2,481+1,913+948+208 = 5,550 ✓；1,741+1,335+768+160 = 4,004 ✓ |

### 4.2 页码约定

- **L002 / L003 / L004 / L005**：PDF 页序 = 期刊页序，直接引用无歧义。
- **L001**：PDF 页序 = 期刊页序 + 1。Evidence Location 中对 L001 标注为 `PDF p.N (journal p.N-1)`，例如 Section 3.11 记为 `PDF p.35 (journal p.34)`。
- **L003**：PDF p.1 = 期刊 p.10。已按 `PDF p.N (journal p.N+9)` 标注。
- 无编造页码。所有 Evidence Location 均为 PDF 中实际存在的小节标题、表号、图号组合。

### 4.3 L001 旋转表格的处理说明

L001 的 11 页表格（PDF pp.8, 9, 12, 16, 18, 21, 24, 26, 29, 30, 32）文字层为旋转存储，直接提取会得到逐词倒序文本。已通过 pypdf 将这些页面旋转 90° 后重新提取，恢复了 Table 1–6 的完整列结构（Food sector / Methodology / Country of study / Key improvements / Outcomes / Limitations / Recommendations / References 等）。

**未做任何倒序猜测。** 表格数值（40–60%、28–100%、2–3 周、20%、15%、70%、40%、99%、3–5 log、5-log、20–40%、12–18%、>90%）均来自旋转恢复后的可读文本，并与 Table 1 的 Limitations 列文本（如 "limited to peanut products; small sample size"）交叉核对。

### 4.4 未编造的项

- **L005 的「区间数」**：原文未明确报告所分析的 interval 数量。Sample Size 字段中未填写该数字，只列出 520 家 establishments / 3,492 次 inspections（原文明确给出）。已在 Extraction Notes 中标注。
- **L005 的 96.1%**：这是作者引用 Läikkö-Roto et al. 的二手统计，不是本文结果。已在 Quantitative Findings 中标注为 `[this last figure is attributed by the author to Läikkö-Roto et al. and is a cited secondary statistic, not a result of this study]`。
- **L001 的 WHO 2024 数据（6 亿、42 万、33 万 DALY、1/10、5 岁以下 40% / 12.5 万、1100 亿美元）**：标注为 `[cited background statistics, NOT study results]`。
- **L002 的 WHO 2015（6 亿、42 万）**、**L003 的澳洲 5.4 百万例 / 12 亿澳元**、**L004 的 EU 45% / 57% / 252 / 7**：均标注为引用背景统计，非研究结果。
- **L001 Section 3.12 的「AI 到 2050 年减少 20–30% 食源性疾病事件」「区块链减少召回 25–30%」**：标注为 `Forward-looking projections ... NOT study results`，并在 Evidence L001-E11 中明确写为「future outlook attributed to other sources」。

---

## 5. 存在问题的文献 / 需注意事项

**无文献判定为「有问题」（无全文不可读、无数据矛盾、无字段无法填写）。** 以下 5 条为提取过程中发现的、后续引用时必须注意的事项。

### 问题 1 — L002 在三个文件夹中重复存放（跨批次去重项）

`Comp Rev Food Sci Food Safe - 2024 - Ze - Risk factors affecting the food safety risk in food business operations for.pdf` 出现在 `食源性疾病`、`全球食品安全`、`风险治理` 三个文件夹。

本批次只处理了 `风险治理` 中的那一份，并将其编号为 L002。后续批次处理 `食源性疾病` 和 `全球食品安全` 时**不得**为其分配新的 Literature ID，应作为 L002 的重复路径处理。否则 18 篇唯一文献会被误记为 21 篇。

### 问题 2 — L001 无自身局限章节

见 §3.1 第 1 点。风险在于：后续若把 Section 3.11 的「领域结构性弱点」当成 L001 的研究局限引用，属于把作者对他人的评价当成自述局限。已在字段内用括注区分。

### 问题 3 — L001 / L003 / L005 无 strengths 章节

见 §3.1 第 3 点。L002 与 L004 填有内容，但均为作者在其他语境下的表述，非正式 strengths 章节。已在字段内注明，不可作为「本研究优势充分」的证据。

### 问题 4 — L003 是访谈研究，几乎所有量化字段结构性为空

L003 无样本量分组、无百分比、无统计检验、无 effect size。Key Variables、Quantitative Findings 均为 `Not reported` 或仅含背景引用。**不得**在后续任何环节把 L003 当作缺陷频率/严重程度的量化证据来源。它能提供的只有机制性/解释性证据（reactive compliance、business survival rationale、CALD 与检查员知识落差）。

### 问题 5 — L004 与 L005 的干预效应方向不一致，且 L004 存在混淆

L004 明确报告定向干预对不符合项的效应方向不统一：protected status 项不符合项上升（0.8%→9.6%），maintenance 与 cleanliness 项下降（p<0.001 / p=0.021），marketing 无显著变化。**不得**概括为「定向干预降低了不符合项」。

同时 L004 自述局限：除 1 项外所有干预都发生在 COVID-19 疫情期间（2020–2021），而 2020–2021 正是该研究用作「疫情前」vs「疫情期间」比较的时段之一，且 2020 年检查数大幅下降。干预效应与疫情效应在时间上重叠，作者本人指出这使干预结果「更难解释」。

L005 的 pre-announcement 效应（2.4x、11.7x）**未经统计检验**——作者自述因同一 establishments 反复检查造成非独立，无法对 pre-announced vs unannounced 做统计检验，只能以 crude numbers 支撑结论。引用该数值时必须同时说明这一点。

---

## 6. 三条额外注意事项（非错误，但影响后续使用）

### 6.1 「非符合项」的含义在 L004 / L005 中不等于「食品安全危害」

芬兰 Oiva 分级中，C/D 的原文定义是 `impairing food safety or misleading consumers`（L005 另加 `major issues` / `failed to correct non-compliances`）。即 C/D 同时包含「危害食品安全」和「误导消费者」两类。L005 的 B 级定义为 `minor issues that do not impair food safety`，因此 B→C/D 被作者称为 "minor → severe"。

**后果：** 把芬兰 C/D 比例当作「食品安全不符合项比例」使用，会混入信息标示类不符合项。L004 Table 2 显示 `information provided on foods`、`display of the inspection report`、`special requirements for specific food products` 三项均属显著上升项，且作者自述这些项的恶化可能来自检查侧重点变化而非企业真实合规下降。已在 Evidence L004-E05 中标注。

### 6.2 L002 的 43 个因子中，5 个只有 1 项研究支持

摘要明确写 `Nearly half of the extracted factors had only been investigated in one study`。同时 inter-rater 一致率仅 77.4%，且包含餐饮场所的研究占 37/44。**后果：** L002 提供的「可用于风险排序的因子清单」其证据基础极不均衡，不能等同于已验证的风险因子集合。作者本人也提出了适用范围受限的问题（§Evidence L002-E12）。

### 6.3 L001 的分级评分属于「叙述性综合」，无 meta 分析

作者明确说明 meta-analysis 不可行。L001 Tables 1–6 中的百分比、log reduction、区间宽度全部是被纳入原始研究的报告值，且 Table 1 明确记录了其中若干项的样本限制（如 "small sample size"）。**后果：** 不能把 L001 当作 effect size 来源；引用其表格数值时必须回到原始研究，而原始研究不在本项目 21 篇清单内。

---

## 7. 本批次未做的事项

- 未写文献综述
- 未写 Introduction / Discussion 任何段落
- 未建立 Research Gap，未判断研究创新性
- 未判断任何文献是否「支持」用户的研究
- 未做跨文献结论比较（`Relationship to Other Included Studies` 全部为 `Not assessed`）
- 未联网检索
- 未新增文献
- 未生成研究不足或空白判断

---

## 8. 下一批次建议

剩余 16 个 PDF 路径（对应约 13 篇唯一文献）位于：`中国监管研究`（12 篇）、`食源性疾病`（2 篇，其中 1 篇为 L002 重复）、`全球食品安全`（2 篇，其中 1 篇为 L002 重复）。

建议顺序：

1. **`全球食品安全` + `HACCP-GMP-ISO` 剩余项** — 若含标准/指南类文本（如 `general principles of food hygiene.pdf`），可校准 `Document Type = Standard/Guideline` 与 `Policy/legal text` 的写法，字段量小。
2. **`中国监管研究` 12 篇，分 4 批 × 3 篇** — 中文期刊，题录字段（作者、期刊、年份、卷期页）需逐项照抄；此批预计可产出与本研究最贴近的中文监管实证证据。
3. **`食源性疾病` 剩余 1 篇** — Introduction 1.1 支撑；注意 L002 去重。
4. 每批结束执行本 QC 文件 §1–§6 的同一套核对项。

**待补充的基准信息（阻塞项，与 Schema §6.1 相同）：** 本文 7 类缺陷编码体系的完整类别名、7 个食品类别的完整名称、严重程度（critical/major/minor）分级标准。补齐前，任何「与本文编码体系对应关系」的判断都不做。
