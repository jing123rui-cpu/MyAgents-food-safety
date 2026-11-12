# Regulation Schema Definition

**Version:** 1.0
**Date:** 2026-07-03
**Module:** `script/regulation_models.py`

---

## 1. Class Hierarchy

```
Regulation (top-level law/standard document)
  鈹?  鈹溾攢鈹€ id: str                     # REG-GB-14881
  鈹溾攢鈹€ title / title_zh            # Bilingual name
  鈹溾攢鈹€ document_type               # national_law | national_standard | ...
  鈹溾攢鈹€ issuing_authority           # 鍥藉鍗敓鍋ュ悍濮斿憳浼?  鈹溾攢鈹€ effective_date              # 2014-06-01
  鈹溾攢鈹€ status                      # effective | draft | replaced | abolished
  鈹溾攢鈹€ scope                       # Applicable domain
  鈹溾攢鈹€ purpose                     # Regulatory objective
  鈹溾攢鈹€ keywords[]                  # Search indexing
  鈹?  鈹斺攢鈹€ chapters[] 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈻?RegulationChapter (chapter / section grouping)
  鈹?  鈹溾攢鈹€ chapter_id                  # e.g. "CH-GB-14881-09"
  鈹溾攢鈹€ title / title_zh
  鈹溾攢鈹€ number                      # "9", "4.1"
  鈹溾攢鈹€ parent_chapter_id           # For nested chapters (nullable)
  鈹?  鈹溾攢鈹€ articles[] 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€ sub_chapters[] (recursive)                  鈹?       鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈻?RegulationArticle (single legal provision)
  鈹?  鈹溾攢鈹€ article_id                  # e.g. "ART-GB-14881-09-03"
  鈹溾攢鈹€ chapter                     # chapter_id reference
  鈹溾攢鈹€ number                      # "9.3", "33(1)"
  鈹溾攢鈹€ title / title_zh
  鈹溾攢鈹€ text                        # Full legal text
  鈹溾攢鈹€ summary                     # One-sentence summary for reports
  鈹溾攢鈹€ keywords[]
  鈹溾攢鈹€ inspection_topics[]         # "process control", "hygiene"
  鈹溾攢鈹€ risk_tags[]                 # "CCP", "traceability", "allergen"
  鈹溾攢鈹€ related_checkpoint_ids[]    # Links to CP-BEV-*-*
  鈹溾攢鈹€ related_rule_ids[]          # Links to RR-CP-BEV-*-*
  鈹溾攢鈹€ severity                    # CRITICAL | HIGH | MEDIUM | LOW
  鈹?  鈹斺攢鈹€ requirements[] 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈻?RegulationRequirement (single inspectable criterion)
  鈹?  鈹溾攢鈹€ requirement_id              # "REQ-GB-14881-09-03-01"
  鈹溾攢鈹€ article_id                  # Parent article reference
  鈹溾攢鈹€ description                 # What must be verified
  鈹溾攢鈹€ inspection_method           # How to verify (observation, document review, measurement)
  鈹溾攢鈹€ required_evidence[]         # What evidence must be collected
  鈹溾攢鈹€ decision_logic              # Deterministic condition
  鈹溾攢鈹€ common_nonconformities[]
  鈹溾攢鈹€ recommended_actions[]
  鈹溾攢鈹€ related_checkpoint_ids[]    # Direct checkpoint mapping
  鈹溾攢鈹€ related_rule_ids[]          # Direct risk rule mapping
  鈹斺攢鈹€ severity                    # CRITICAL | HIGH | MEDIUM | LOW
```

---

## 2. UML Diagram

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                 Regulation                     鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?- id: str                                      鈹?鈹?- title: str                                   鈹?鈹?- title_zh: str                                鈹?鈹?- document_type: DocumentType                  鈹?鈹?- issuing_authority: str                       鈹?鈹?- effective_date: str                          鈹?鈹?- status: RegulationStatus                     鈹?鈹?- scope: str                                   鈹?鈹?- purpose: str                                 鈹?鈹?- keywords: List[str]                          鈹?鈹?- last_revision: str                           鈹?鈹?- chapters: List[RegulationChapter]            鈹?鈹?- metadata: Dict[str, Any]                     鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?             鈹?1
             鈹?contains
             鈹?*
             鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?             RegulationChapter                  鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?- chapter_id: str                              鈹?鈹?- title: str                                   鈹?鈹?- title_zh: str                                鈹?鈹?- number: str                                  鈹?鈹?- parent_chapter_id: Optional[str]             鈹?鈹?- articles: List[RegulationArticle]            鈹?鈹?- sub_chapters: List[RegulationChapter]        鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?             鈹?1
             鈹?contains
             鈹?*
             鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?             RegulationArticle                  鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?- article_id: str                              鈹?鈹?- chapter: str                                 鈹?鈹?- number: str                                  鈹?鈹?- title: str                                   鈹?鈹?- title_zh: str                                鈹?鈹?- text: str                                    鈹?鈹?- summary: str                                 鈹?鈹?- keywords: List[str]                          鈹?鈹?- inspection_topics: List[str]                 鈹?鈹?- risk_tags: List[str]                         鈹?鈹?- related_checkpoint_ids: List[str]            鈹?鈹?- related_rule_ids: List[str]                  鈹?鈹?- severity: SeverityLevel                      鈹?鈹?- requirements: List[RegulationRequirement]    鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?             鈹?1
             鈹?decomposes to
             鈹?*
             鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?          RegulationRequirement                 鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?- requirement_id: str                          鈹?鈹?- article_id: str                              鈹?鈹?- description: str                             鈹?鈹?- inspection_method: str                       鈹?鈹?- required_evidence: List[str]                 鈹?鈹?- decision_logic: str                          鈹?鈹?- common_nonconformities: List[str]            鈹?鈹?- recommended_actions: List[str]               鈹?鈹?- related_checkpoint_ids: List[str]            鈹?鈹?- related_rule_ids: List[str]                  鈹?鈹?- severity: SeverityLevel                      鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?maps to
       鈹?       鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?   Checkpoint     鈹?   鈹?   RiskRule      鈹?鈹? (CP-BEV-*-NNN)  鈹傗梽鈹€鈹€鈻衡攤 (RR-CP-BEV-*-NNN)鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?                              鈻?                      鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                      鈹?   RuleEngine         鈹?                      鈹?COMPLIANT/NON_COMPLIANT鈹?                      鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?           RegulationCitation                   鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?- regulation_id: str                           鈹?鈹?- title_zh: str                                鈹?鈹?- article_numbers: List[str]                   鈹?鈹?- article_texts: List[str]                     鈹?鈹?- chapter: str                                 鈹?鈹?- severity: SeverityLevel                      鈹?鈹?- reason: str                                  鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?        RegulationKnowledgeBase                 鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?- regulations: Dict[str, Regulation]           鈹?鈹?- chapters: Dict[str, RegulationChapter]       鈹?鈹?- articles: Dict[str, RegulationArticle]       鈹?鈹?- requirements: Dict[str, RegulationRequirement]鈹?鈹?- warnings: List[str]                          鈹?鈹?- errors: List[str]                            鈹?鈹?                                               鈹?鈹?+ get_article(id) -> RegulationArticle         鈹?鈹?+ get_requirement(id) -> RegulationRequirement 鈹?鈹?+ get_checkpoint_requirements(cp_id) -> List   鈹?鈹?+ get_rule_requirements(rule_id) -> List       鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

---

## 3. Field Reference

### 3.1 Regulation

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | yes | Unique regulation code, e.g. `REG-GB-14881` |
| `title` | str | yes | English title |
| `title_zh` | str | yes | Chinese title |
| `document_type` | DocumentType | yes | Classification of the legal document |
| `issuing_authority` | str | yes | Name of the issuing government body |
| `effective_date` | str | yes | ISO date `YYYY-MM-DD` when the regulation became effective |
| `status` | RegulationStatus | yes | Current lifecycle status |
| `scope` | str | no | Regulatory scope statement (field of application) |
| `purpose` | str | no | Regulatory purpose statement |
| `keywords` | List[str] | no | Search keywords |
| `last_revision` | str | no | ISO date of most recent revision |
| `chapters` | List[RegulationChapter] | no | Contained chapters |
| `metadata` | Dict[str, Any] | no | Extensible metadata |

### 3.2 RegulationChapter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chapter_id` | str | yes | Unique chapter ID, e.g. `CH-GB-14881-09` |
| `title` | str | yes | English title |
| `title_zh` | str | no | Chinese title |
| `number` | str | yes | Chapter/section number, e.g. `"9"`, `"4.1"` |
| `parent_chapter_id` | Optional[str] | no | For nested chapter hierarchies |
| `articles` | List[RegulationArticle] | no | Articles in this chapter |
| `sub_chapters` | List[RegulationChapter] | no | Nested sub-chapters |

### 3.3 RegulationArticle

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `article_id` | str | yes | Unique article ID, e.g. `ART-GB-14881-09-03` |
| `chapter` | str | yes | Chapter ID this article belongs to |
| `number` | str | yes | Article number as it appears in the legal text, e.g. `"9.3"`, `"33"` |
| `title` | str | no | English title |
| `title_zh` | str | no | Chinese title |
| `text` | str | no | Full verbatim text of the article |
| `summary` | str | no | One-sentence summary for audit reports |
| `keywords` | List[str] | no | Keywords relevant to this article |
| `inspection_topics` | List[str] | no | Topics this article covers for inspection (e.g. `"temperature control"`, `"traceability"`) |
| `risk_tags` | List[str] | no | Risk-related tags (e.g. `"CCP"`, `"allergen"`, `"microbiology"`) |
| `related_checkpoint_ids` | List[str] | no | Checkpoints that this article maps to |
| `related_rule_ids` | List[str] | no | Risk rules that cite this article |
| `severity` | SeverityLevel | no | Default severity if violated |
| `requirements` | List[RegulationRequirement] | no | Decomposed inspectable requirements |

### 3.4 RegulationRequirement

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `requirement_id` | str | yes | Unique requirement ID, e.g. `REQ-GB-14881-09-03-01` |
| `article_id` | str | yes | Parent article ID |
| `description` | str | yes | What must be verified 鈥?the inspection criterion |
| `inspection_method` | str | no | How to verify (observation, document review, measurement, test, interview) |
| `required_evidence` | List[str] | no | Evidence items that must be collected |
| `decision_logic` | str | no | Deterministic condition for PASS / FAIL evaluation |
| `common_nonconformities` | List[str] | no | Typical non-conformities observed during audits |
| `recommended_actions` | List[str] | no | Recommended corrective/preventive actions |
| `related_checkpoint_ids` | List[str] | no | Direct mapping to checkpoints |
| `related_rule_ids` | List[str] | no | Direct mapping to risk rules |
| `severity` | SeverityLevel | no | Default severity if violated |

### 3.5 RegulationCitation

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `regulation_id` | str | yes | Regulation code |
| `title_zh` | str | no | Chinese title for display |
| `article_numbers` | List[str] | no | Cited article numbers |
| `article_texts` | List[str] | no | Cited article text snippets |
| `chapter` | str | no | Chapter reference |
| `severity` | SeverityLevel | no | Severity context |
| `reason` | str | no | Reasoning for citing this regulation |

### 3.6 RegulationKnowledgeBase

| Method | Returns | Description |
|--------|---------|-------------|
| `get_article(article_id)` | `Optional[RegulationArticle]` | Lookup by article ID |
| `get_requirement(requirement_id)` | `Optional[RegulationRequirement]` | Lookup by requirement ID |
| `get_checkpoint_requirements(checkpoint_id)` | `List[RegulationRequirement]` | All requirements for a checkpoint |
| `get_rule_requirements(rule_id)` | `List[RegulationRequirement]` | All requirements for a risk rule |

---

## 4. Enums

### 4.1 DocumentType

| Value | Description |
|-------|-------------|
| `national_law` | 娉曞緥 鈥?enacted by the NPC Standing Committee |
| `national_standard` | 鍥藉鏍囧噯 鈥?GB series issued by NHC/SAMR |
| `administrative_regulation` | 琛屾斂娉曡 鈥?issued by SAMR or other ministries |
| `industry_standard` | 琛屼笟鏍囧噯 鈥?issued by industry bodies |
| `guideline` | 鎸囧鎬ф枃浠?鈥?non-binding guidance |

### 4.2 RegulationStatus

| Value | Description |
|-------|-------------|
| `effective` | 鐜拌鏈夋晥 鈥?currently in force |
| `draft` | 寰佹眰鎰忚绋?鈥?draft for public comment |
| `replaced` | 琚浛浠?鈥?superseded by a newer version |
| `abolished` | 搴熸 鈥?formally abolished |

### 4.3 SeverityLevel

| Value | Description | Score Impact |
|-------|-------------|-------------|
| `CRITICAL` | 椋熷搧瀹夊叏鐩存帴鐩稿叧 | Rule 鈫?NON_COMPLIANT, score 0.0 |
| `HIGH` | 绯荤粺鎬ц姹?| Rule 鈫?NON_COMPLIANT, score 0.0 |
| `MEDIUM` | 绠＄悊鎬ц姹?| Rule 鈫?NON_COMPLIANT, score 0.0 |
| `LOW` | 寤鸿鎬ц姹?| Rule 鈫?COMPLIANT, score 1.0 |

---

## 5. ID Naming Convention

| Model | Pattern | Example |
|-------|---------|---------|
| Regulation | `REG-{CODE}` | `REG-GB-14881` |
| Chapter | `CH-{REG_CODE}-{NUMBER}` | `CH-GB-14881-09` |
| Article | `ART-{REG_CODE}-{CH_NUMBER}-{ART_NUMBER}` | `ART-GB-14881-09-03` |
| Requirement | `REQ-{REG_CODE}-{CH_NUMBER}-{ART_NUMBER}-{SEQ}` | `REQ-GB-14881-09-03-01` |
| Citation | Embedded in `EvaluationResult.violated_laws` | `REG-GB-14881 搂9.3` |

---

## 6. YAML Example

```yaml
id: REG-GB-14881
title: National Food Safety Standard 鈥?General Hygiene Code for Food Production
title_zh: 椋熷搧瀹夊叏鍥藉鏍囧噯 椋熷搧鐢熶骇閫氱敤鍗敓瑙勮寖
document_type: national_standard
issuing_authority: 涓崕浜烘皯鍏卞拰鍥藉浗瀹跺崼鐢熷仴搴峰鍛樹細
effective_date: "2014-06-01"
status: effective
scope: 鎵€鏈夐鍝佺敓浜т紒涓氱殑鐢熶骇鏉′欢銆佺敓浜ц繃绋嬫帶鍒躲€佸崼鐢熺鐞?
chapters:
  - chapter_id: CH-GB-14881-09
    title: Production Process Control
    title_zh: 鐢熶骇杩囩▼鎺у埗
    number: "9"
    articles:
      - article_id: ART-GB-14881-09-03
        number: "9.3"
        text: ""
        severity: HIGH
        requirements:
          - requirement_id: REQ-GB-14881-09-03-01
            description: CCP monitoring records must be maintained
            decision_logic: CCP records complete and within limits
```

---

## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-03 | Initial release 鈥?regulation schema definition |
