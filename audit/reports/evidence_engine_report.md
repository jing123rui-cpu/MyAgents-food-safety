# Evidence Engine Report

## Files Created / Modified

| File | Change |
|------|--------|
| `script/models.py` | Added `EvidenceType` enum, `Evidence` dataclass |
| `script/evidence.py` | **Created** 鈥?`EvidenceCollection`, `validate_evidence()` |
| `script/workflow.py` | Added `evidence: List[Evidence]` to `InspectionContext` |
| `script/__init__.py` | Exported `Evidence`, `EvidenceType`, `EvidenceCollection`, `validate_evidence` |

---

## Evidence Model

```python
class EvidenceType(str, Enum):
    OBSERVATION  = "OBSERVATION"   # Inspector observation note
    PHOTO        = "PHOTO"         # Uploaded photo
    DOCUMENT     = "DOCUMENT"      # Document / PDF
    MEASUREMENT  = "MEASUREMENT"   # Sensor reading / gauge value
    LAB_REPORT   = "LAB_REPORT"    # Laboratory analysis report
    VIDEO        = "VIDEO"         # Video recording
    SYSTEM_RECORD = "SYSTEM_RECORD"  # ERP / MES / QMS export


@dataclass
class Evidence:
    id: str
    evidence_type: EvidenceType
    checkpoint_id: str
    description: str
    source: str = ""
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

## Evidence Lifecycle

```
  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?Collect  鈹? 鈫?inspector / system 鈫?EvidenceCollection.add()
  鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹?       鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?Validate 鈹? 鈫?validate_evidence()
  鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹?       鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?Store in     鈹? 鈫?InspectionContext.evidence
  鈹?Context      鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?Consume by   鈹? 鈫?Decision Engine / AI Agent (future)
  鈹?Decision     鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

No automatic collection 鈥?evidence is added explicitly by the caller.

---

## EvidenceCollection API

| Method | Signature | Description |
|--------|-----------|-------------|
| `add` | `(evidence: Evidence)` | Add unique evidence; raises `ValueError` on duplicate ID |
| `add_all` | `(items: List[Evidence]) -> List[str]` | Bulk add; returns list of skipped (duplicate) IDs |
| `remove` | `(evidence_id: str)` | Remove by ID; raises `KeyError` if missing |
| `get` | `(evidence_id: str) -> Optional[Evidence]` | Lookup by ID |
| `list` | `() -> List[Evidence]` | All items in insertion order |
| `count` | `() -> int` | Number of items |

---

## Supported Evidence Types

| Type | Example use case |
|------|-----------------|
| `OBSERVATION` | "Storage room temperature measured at 28 掳C" |
| `PHOTO` | `IMG_20260703_1430.jpg` 鈥?warehouse shelf photo |
| `DOCUMENT` | `supplier_license_12345.pdf` |
| `MEASUREMENT` | `{"temp": 25.3, "humidity": 62}` |
| `LAB_REPORT` | `lab_result_20260701_batch45.pdf` |
| `VIDEO` | `filling_line_20260703.mp4` |
| `SYSTEM_RECORD` | ERP export of last 30 days of temperature logs |

---

## Validation Logic (`validate_evidence`)

| Check | Condition | Warning |
|-------|-----------|---------|
| Duplicate ID | Two items share the same `id` | `"Duplicate evidence ID '{id}'"` |
| Empty description | `description.strip()` is empty | `"Evidence '{id}' has an empty description"` |
| Invalid type | `evidence_type.value` not in `EvidenceType` | `"Evidence '{id}' has invalid type '...'"` |
| Missing checkpoint | `checkpoint_id` not in repository (if repo provided) | `"Evidence '{id}' references unknown checkpoint '...'"` |
| Broken attachment | Attachment path is absolute and does not exist | `"Evidence '{id}' attachment not found: {path}"` |

---

## Future Integration

| Feature | Description |
|---------|-------------|
| **Image analysis** | Extract text / objects from `PHOTO` evidence via OCR |
| **OCR pipeline** | Process `DOCUMENT` attachments through OCR and store result in `metadata["ocr_text"]` |
| **Measurement parsing** | Normalise `MEASUREMENT` values into structured `metadata["normalised"]` |
| **Attachment hashing** | Compute SHA-256 of attachments for integrity verification |
| **Evidence timeline** | Sort evidence by timestamp for chronogical reconstruction |

---

## Usage Example

```python
from core.models import Evidence, EvidenceType
from core.evidence import EvidenceCollection, validate_evidence

collection = EvidenceCollection()
collection.add(Evidence(
    id="EVID-RM-001-01",
    evidence_type=EvidenceType.PHOTO,
    checkpoint_id="CP-BEV-RM-001",
    description="渚涘簲鍟嗙敓浜ц鍙瘉澶嶅嵃浠?,
    source="鐜板満鎷嶆憚",
    attachments=["photos/license_001.jpg"],
))

ctx = workflow.build_context(request)
ctx.evidence = collection.list()

warnings = validate_evidence(ctx.evidence, repository=repo)
```

