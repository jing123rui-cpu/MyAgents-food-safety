# Literature Batch 02 — QC Report

**Batch:** 02
**Scope:** 本批次仅分析 `全球食品安全` 与 `食源性疾病` 两个文件夹中的 4 个 PDF。
**分析目标：** 客观记录每篇文献研究了什么，重点提取研究范围、疾病负担、数量、死亡、DALY/YLL/YLD、病原体、食品类别、风险因素、数据来源、估计方法、时间范围、研究对象、主要发现、不确定性、局限。
**输出文件：** `Literature_Batch_02.xlsx`（Sheet 1: Literature Matrix；Sheet 2: Evidence Details）
**Schema 依据：** `output\Literature_Matrix_Schema.md` v1.0（Excel 结构与 Batch 01 完全一致：34 列 + 6 列）
**生成日期：** 2026-09-30

---

## 1. 完成情况汇总

| 指标 | 数值 |
|---|---|
| 本批次计划处理 PDF | 4 |
| 实际处理 PDF | 4 |
| 其中重复文件（已登记，不新建行） | 2 |
| **新增唯一文献** | **2（L006, L007）** |
| 成功读取全文（Full text） | 4 |
| Abstract-only | 0 |
| 全文不可读 | 0 |
| 存在问题的文献 | 0（另有 4 条需注意事项，见 §5） |
| Literature Matrix 行数 | 2（L006–L007） |
| Literature Matrix 字段数 | 34 |
| Evidence Details 行数 | 32 |
| 空单元格 | 0 |
| 联网检索次数 | 0 |
| 新增文献数 | 0 |

### 文件处理结果

| 文件夹 | 文件名 | 页数 | 提取字符数 | 处理结果 |
|---|---|---|---|---|
| 全球食品安全 | `general principles of food hygiene.pdf` | 60 | 143,066 | 新建 L006 |
| 全球食品安全 | `Comp Rev Food Sci Food Safe - 2024 - Ze - Risk factors….pdf` | 20 | 98,716 | 重复文件 → 登记为 L002 |
| 食源性疾病 | `资源有限环境中食源性疾病的流行病学与控制.pdf` | 17 | 121,448 | 新建 L007 |
| 食源性疾病 | `Comp Rev Food Sci Food Safe - 2024 - Ze - Risk factors….pdf` | 20 | 98,716 | 重复文件 → 登记为 L002 |

L006 有 3 页（PDF pp.2, 58, 59）无文本层。已核对：p.2 位于封面块内部，pp.58-59 为封底与许可/销售页，**规范性正文无任何内容丢失**。

---

## 2. 重复文件登记（本批次不新建行）

本批次 4 个 PDF 路径实际对应 **2 篇唯一文献**。

### 2.1 Ze et al. (2024) — 第 3 份副本

同一篇文章现在已在 3 个文件夹中出现：

| # | 文件夹 | 文件 SHA-256 | 提取文本 SHA-256 |
|---|---|---|---|
| 1 | 风险治理 | `6607B662…34D4` | — （Batch 01 已登记为 **L002**） |
| 2 | 全球食品安全 | `66AEB5CC…F1EDC4` | `989865BD…B3B99F6` |
| 3 | 食源性疾病 | `740FD065…99C280E` | 同上文本哈希的变体 |

**验证方法与结论：** 三份 PDF 的二进制哈希不同，但提取出的文本逐行比对后，差异**仅出现在 Wiley 页脚下载日期戳**（`[20/08/2026]` vs `[24/08/2026]`），共 58 行，全部为同一行内容的日期差异。三份的字符数均为 98,716，章节结构、小节标题、Table 1–2、Figure 1、全部数值完全一致。

**处理：** 未为这两份文件分配新的 Literature ID。矩阵中 L002 仍只有一行。Batch 01 QC §5 已预警此项，此处完成闭环。

### 2.2 累计去重台账（截至 Batch 02）

| Literature ID | 唯一文献 | 出现的文件夹数 | 已登记路径 |
|---|---|---|---|
| L002 | Ze et al. 2024, Compr Rev Food Sci Food Saf | 3 | 风险治理；全球食品安全；食源性疾病 |

21 个 PDF 路径 → 截至 Batch 02 已处理 9 个路径，对应 **7 篇唯一文献**（L001–L007，其中 L002 占 3 个路径）。剩余 12 个路径在 `中国监管研究`，无重复。

---

## 3. Document Type 判定（本批次重点）

| Literature ID | Document Type | 判定依据（原文位置） |
|---|---|---|
| L006 | **Standard/Guideline** | 封面印 `GENERAL PRINCIPLES OF FOOD HYGIENE (CXC 1-1969)` / `SERIES EDITION` / `Codex Alimentarius Code of Practice, No. CXC 1-1969`；署名 FAO 与 WHO；无作者、无摘要、无研究结果 |
| L007 | **Review** | PDF p.1 文章类型标签即 `Review`；摘要自述 `This narrative review provides an overview of current evidence…`；方法节 `This study was conducted as a narrative review`；`a qualitative narrative synthesis approach was adopted rather than quantitative pooling of findings` |

**按要求执行的两条判定：**

- **L006 未被当作 Original Research。** 该文件是 FAO/WHO 食品法典委员会发布的规范性国际行为准则，不是研究。所有研究设计类字段（Study Population、Sample Size、Study Period、Data Source、Key Variables、Statistical Methods、Quantitative Findings、Authors' Interpretation）均填 `Not applicable` / `Not reported`，并在 Extraction Notes 中写明原因。
- **L007 未被当作 Original Research。** 虽然文件名与内容都涉及阿富汗疫情数据，但作者本人不采集数据、不做统计分析、不做定量合并。所有阿富汗数字都是**转引自他人研究**。已在 Key Findings 第 1 条与 Quantitative Findings 顶部明确标注。

**L007 的三个 No 判定说明：**

| 字段 | 取值 | 理由 |
|---|---|---|
| `Regulatory Inspection Data?` | No | 文中确有监管制度描述（三个政府部门、无风险导向检查、`all establishments are inspected uniformly`、83% 屠宰点持证但监测不足），但这些是**引述的制度陈述**，本文未使用任何检查记录作为数据。 |
| `Non-compliance Findings Used?` | No | 文中讨论 HACCP 未实施、卫生标准执行不到位、持证但不合规，但**未把不符合项记录作为分析对象**。 |
| `Enterprise-level Data?` | No | 本文数据单元是文献与机构报告。仅个别底层研究为企业层面（Herat 182 家屠宰点）。 |

---

## 4. 重点提取项的实际覆盖情况（对照本批次指定的 15 个重点）

用户指定的 15 个重点在两篇文献中的实际存在情况如下。**不存在的一律填 `Not reported` 或 `Not applicable`，未做任何补充。**

| 重点提取项 | L006（Codex CXC 1-1969） | L007（Zahir 2026 JFP） |
|---|---|---|
| 1. 全球/地区研究范围 | International / global（Codex 公约；无研究国别） | Afghanistan 为主 + 肯尼亚、津巴布韦、孟加拉、尼泊尔、印度、尼日利亚、埃塞俄比亚、巴西 |
| 2. 食源性疾病负担 | **Not reported**（全文无任何流行病学数据） | 有，但全部为**转引**，且明确声明阿富汗无国家估计 |
| 3. 疾病数量 | **Not reported** | 转引：全球近 6 亿例/年；阿富汗 2024 年 AWD 130,890 例；2022 年 >50 万例 |
| 4. 死亡数量 | **Not reported** | 转引：全球 42 万/年；东南亚及非洲 5 岁以下儿童 12.5 万/年；阿富汗 2024 年 AWD 62 例；Nimroz 2007 暴发 17/83 死亡 |
| 5. DALYs / YLL / YLD | **Not reported** | **DALY 无任何数值**。仅定性提及（引用 Kirk et al., 2015；称 1999 年以来传染病 DALY 显著下降但未给数）。**YLL、YLD 全文未出现** |
| 6. 病原体 | 无（规范性文件） | Salmonella spp.；E. coli（含 O157:H7）；L. monocytogenes；Campylobacter spp.；Hepatitis A/E；V. cholerae；Y. pestis；Giardia lamblia；E. histolytica；H. nana；A. lumbricoides；T. gondii；T. trichiura；E. vermicularis；Shigella；S. aureus；耐药菌 |
| 7. 食品类别 | 覆盖全链条（生产/加工/制造/包装/储运/零售/餐饮/运输），无单一类别 | 畜产品（肉、禽、蛋、奶、鱼、蜂蜜）、生鲜果蔬、街边即食食品、快餐、小麦粉、食盐、饮用水 |
| 8. 风险因素 | 规范性要求：危害分析、CCP、关键限、监测、纠正、验证、记录 | 卫生差、意识缺乏、监管薄弱、基础设施（冷链/实验室）、非正规市场、AMR、贫困与经济胁迫 |
| 9. 数据来源 | **Not applicable**（无数据） | 文献库（Scopus/WoS/PubMed/Google Scholar）+ WHO/FAO/UNICEF 报告 + 参考文献手动筛选 |
| 10. 估计方法 | **Not applicable** | 叙述性定性主题综合；**明确不做定量合并**；无统计检验、无软件、无 p 值、无效应量 |
| 11. 时间范围 | 版本沿革 1969/1999/1997/2003/2020/2022/2011；本版 2023 | 纳入文献 2010–2026；底层数据 2007-12 至 2026-02 |
| 12. 研究对象 | **Not applicable** | **Not applicable as a sampled population**；分析单元为已发表文献 |
| 13. 主要发现 | 见 L006 Key Findings 1–5（全部为规范性条款） | 见 L007 Key Findings 1–5（全部为转引数据） |
| 14. 不确定性 | 明确声明不提供场景特定指引；要求由主管当局评估「likelihood and severity」但不给数值 | 「informative of variable quality」「indicative of prevailing patterns rather than precise estimates of disease burden」 |
| 15. 研究局限 | 无局限章节（规范性文件）；Section 4 有明确范围声明 | 三处作者自述：Quality considerations、Strengths and limitations of the review、以及"无国家估计"的范围声明 |

---

## 5. 存在问题的文献 / 需注意事项

**无文献判定为「有问题」。** 以下 4 条为提取过程中的发现，后续引用时必须注意。

### 问题 1 — L006 完全没有流行病学数据

这是本批次最需要警惕的一条。L006 是 60 页的 FAO/WHO 食品卫生通则，篇幅大、章节多（19 章 + 4 个附录），极易被误当作「全球食品安全」背景文献引用。

**已做的全文核查：** 对全部 60 页检索 `DALY`、`600 million`、`420 000`、`125 000`、`incidence`、`prevalence`、`burden of disease`、`estimat`，**无任何实质性命中**。全文唯一一次出现 "burden" 是在 Section 18.2，指「certain types of FBOs 的记录负担」，与疾病负担无关。

**后果：** L006 不能支撑任何关于疾病数量、死亡数、DALY、病原体、食品类别风险或风险因素的陈述。它只能作为**规范性框架来源**（GHP/HACCP 条款、GHP 与 CCP 的九行对比表、清洁消毒与虫害控制的目标定义、小微企业灵活性条款）。已在 Quantitative Findings 字段与 Evidence L006-E02 中显式写明这一「不存在」。

### 问题 2 — L007 的负担数字全部是转引，且论文自己声明无国家估计

L007 有大量看似「一手」的阿富汗数字（污染率、血清阳性率、暴发数），但作者是 narrative review，**未采集任何数据**。

论文自身在两处明确限制：
- `Afghanistan lacks specific national estimates for FBDs`
- `Although accurate national estimates of the economic cost of FBDs are currently unavailable...`
- `conclusions should be interpreted as indicative of prevailing patterns rather than precise estimates of disease burden`

**后果：** 引用任一阿富汗数字时，必须同时标注三点：(a) 原始出处（如 Ahmadi et al., 2024）；(b) 论文自身的限制声明；(c) 该数字属「indicative of patterns」而非「burden estimate」。论文中还明确写明不同研究间的污染率差异 `highlight methodological variability rather than consistent pathogen distribution patterns`，**不得**把这些数字平均、合并或排序。

### 问题 3 — L007 的 DALY 数据完全缺失

用户把 DALYs / YLL / YLD 列为重点提取项。实际情况：

- **DALY：全文无数值。** 仅两处定性提及（引用 Kirk et al., 2015；称 1999 年以来总体传染病 DALY「显著下降」但未给数）。
- **YLL、YLD：全文未出现。**
- 论文反而把 DALY 列为**尚待测量**的项目。

**后果：** 本批次没有任何一篇文献可提供 DALY / YLL / YLD 数值。已在 L007 的 Quantitative Findings 末尾单列一段说明，Evidence L007-E04 单独记录。

**另需注意：本批次两篇文献的负担数据集并不相同。** L007 未出现 L001（Batch 01）中的「1 in 10 people」「33 million DALYs」「5 岁以下占 40% 病例」等数字。**不得假定两篇的负担数字集一致或可互补。**

### 问题 4 — L006 无 PDF 文本的 3 页已核对为非内容页

PDF pp.2, 58, 59 无文本层。逐页核对：p.2 位于封面与扉页之间的空白块，pp.58-59 为封底、许可条款与销售信息。**规范性正文（PDF pp.7-51，印刷页 1-45）全部有文本，无内容缺失。** 已在 `Full-text Readable?` 字段注明。

---

## 6. 其他需记录事项

### 6.1 L007 文件名与语言不一致

文件名 `资源有限环境中食源性疾病的流行病学与控制.pdf` 为中文，但 **PDF 全文为英文**（Journal of Food Protection, Elsevier）。文件名是标题的中文译名。已在 Extraction Notes 首要位置注明，避免后续按中文文献处理或误判。

### 6.2 L007 存在编辑缺陷与来源质量问题

三点，均为客观可核实的观察：

1. **检索策略段落重复。** PDF p.2 中，以 `Relevant literature was identified through electronic searches of major scientific databases, including Scopus, Web of Science, PubMed, and Google Scholar…` 开头的段落**在同页出现两次**（仅引导句略异）。
2. **Table 1 中有非同行评议来源。** 食盐碘缺乏/重金属一项引用 `Pajhwok News, 2025`，为新闻机构。
3. **大量参考文献为 2025–2026 年**，与所综合的大部分基础证据存在时间落差。

### 6.3 L007 未报告纳入研究数量

论文给出数据库、时间范围（2010–2026）、详细纳入排除标准，以及「通过手动筛选参考文献补充」，但**未报告检索到多少条、筛除多少条、纳入多少条，也无 PRISMA 流程图**。因此 `Sample Size` 填 `Not reported`，并在 Limitations 中补记这一条（标注为提取者观察，非作者陈述）。已在 Evidence L007-E18 单独记录。

### 6.4 L007 声明使用了生成式 AI

PDF p.14：`During the preparation of this work, the authors used ChatGPT to improve the readability and language of the manuscript. After using this tool, the authors reviewed and edited the content as needed.` 已记入 Extraction Notes。

### 6.5 L006 的页码换算

PDF 页序 = 印刷页序 + 6（封面占 PDF pp.1-6，印刷页 1 起于 PDF p.7）。已核验锚点：Section 1 = PDF p.7；Section 2 = PDF p.8；Section 5 = PDF p.10；Section 6 = PDF pp.12-14；Section 11 = PDF p.23；Section 17 = PDF p.39；Section 18.1 = PDF pp.39-40；Section 18.2 = PDF pp.40-41；Annex I Table 1 = PDF p.50；Annex IV = PDF pp.49-51。所有 L006 的 Evidence Location 均已按此换算并同时给出 PDF 页码。

### 6.6 L006 本版新增内容

封面后附注：`This edition contains new content (Annex IV, Figure 1 and Table 1) which introduces tools to determine the critical control points`。引用 CCP 判定工具时须注明为 2023 版新增，不可回溯到 2020/2022 版。已记入 Evidence L006-E14。

---

## 7. 数值核对记录

| 项目 | 记录值 | 原文位置 | 核对结果 |
|---|---|---|---|
| L007 纳入研究数 | 未报告 | PDF pp.2-3 | 确认全文无计数、无 PRISMA 图 |
| L007 检索时间窗 | 2010–2026 | PDF p.2 | 一致（文中该句重复出现两次） |
| L007 全球负担 | 近 6 亿例 / 42 万死亡 | PDF pp.1, 7 | 一致（两处，均为转引 Tzachor 2024 / WHO） |
| L007 阿富汗 2024 | AWD 130,890 例、62 死亡 | PDF p.7 | 一致 |
| L007 2022 | AWD >500,000 例 | PDF p.6, Table 1 | 一致 |
| L007 Nimroz 2007 | 83 例疑似、17 例死亡（20.5%） | PDF p.4 | 17/83 = 20.48% ≈ 20.5% ✓ |
| L007 贾拉拉巴德寄生虫 | 48.8%（294/603） | PDF p.4 | 294/603 = 48.76% ≈ 48.8% ✓ |
| L007 弓形虫血清 | 48.03%（207/431） | PDF p.4 | 207/431 = 48.03% ✓ |
| L007 加兹尼贾第鞭毛虫 | 21.2%（52/245） | PDF p.4 | 52/245 = 21.22% ≈ 21.2% ✓ |
| L007 贾拉拉巴德寄生虫构成 | 35.8+34.3+22.5+5.3+1.8+0.3 = 100.0 | PDF p.4 | 求和 ✓ |
| L006 流行病学数据 | 无 | 全文 60 页 | 关键词检索无实质命中 |

**未编造项：** L007 的 YLL、YLD、DALY 数值（原文无 → 记为无）；L006 的任何流行病学数值（原文无 → 记为无）；L007 的「无国家 DALY 估计」这一事实已作为发现记录，而非填补数值。

---

## 8. Evidence Details 分布（32 条）

| Literature ID | 条数 |
|---|---|
| L006 | 14 |
| L007 | 18 |

| Evidence Type | L006 | L007 | 合计 |
|---|---|---|---|
| Regulatory evidence | 14 | 0 | 14 |
| Empirical evidence | 0 | 9 | 9 |
| Background evidence | 0 | 4 | 4 |
| Methodological evidence | 0 | 4 | 4 |
| Comparative evidence | 0 | 1 | 1 |
| Mechanism/process evidence | 0 | 0 | 0 |
| Contradictory/alternative evidence | 0 | 0 | 0 |
| **合计** | **14** | **18** | **32** |

L006 全部为 `Regulatory evidence`（规范性条款），无一条 `Empirical evidence`——与其 Document Type 一致。

---

## 9. 本批次未做的事项

- 未写 Introduction
- 未写文献综述
- 未做 Research Gap
- 未判断任何文献是否支持用户的研究
- 未做跨文献结论比较（`Relationship to Other Included Studies` 全部为 `Not assessed`）
- 未为「食品安全是全球问题」「食源性疾病负担很重」寻找支持性证据；L006 完全没有此类内容，已如实记录为无
- 未联网检索
- 未新增文献
- 未为重复文件分配新 Literature ID

---

## 10. 下一批次

剩余 12 个 PDF 全部位于 `中国监管研究`，无重复。累计状态：

| 项 | 路径数 | 唯一文献数 |
|---|---|---|
| PDF 路径总数 | 21 | — |
| Batch 01 已处理（HACCP-GMP-ISO 1 + 风险治理 1 + 监管检查数据 3） | 5 | 5（L001–L005） |
| Batch 02 已处理（全球食品安全 2 + 食源性疾病 2） | 4 | 2（L006、L007；另 2 个路径为 L002 重复） |
| **已处理小计** | **9** | **7** |
| **待处理（全部位于 \中国监管研究\，无重复）** | **12** | **12** |
| 校验 | 9 + 12 = 21 | 7 + 12 = 19 篇唯一文献 |

建议：\中国监管研究\ 12 篇分 4 批 × 3 篇处理。

**待补充的基准信息（阻塞项）：** 本文 7 类缺陷编码体系的完整类别名、7 个食品类别的完整名称、严重程度（critical/major/minor）分级标准。
