# FastAPI REST API Server Report 鈥?Sprint 24

## Overview

- **Sprint:** 24
- **Objective:** Expose the FoodAuditAgent runtime through a REST API.
- **Server:** FastAPI + uvicorn
- **Port:** 8000 (default)

---

## API Architecture

```
Client  鈹€鈹€HTTP鈹€鈹€>  FastAPI (api/server.py)  鈹€鈹€>  FoodAuditAgent (script/)
                         鈹?                    鈹屸攢鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹?                    鈹? Pydantic 鈹?                    鈹? Schemas  鈹?                    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

The agent is initialised once during application startup via FastAPI lifespan events and remains in memory for the lifetime of the server process.

---

## Endpoints

| Method | Path | Description | Status Codes |
|--------|------|-------------|-------------|
| GET | `/` | Root info | 200 |
| GET | `/health` | Agent health status | 200, 500 |
| POST | `/search` | Search checkpoints | 200, 422, 500 |
| POST | `/inspect` | Full inspection with optional evidence | 200, 422, 500 |

### API Documentation (auto-generated)

| URL | Description |
|-----|-------------|
| `/docs` | Swagger UI |
| `/redoc` | ReDoc |
| `/openapi.json` | OpenAPI schema |

---

## Request / Response Examples

### GET /

**Request:**
```
curl http://localhost:8000/
```

**Response (200):**
```json
{
  "name": "Food Audit Agent",
  "version": "1.0.0",
  "status": "running",
  "timestamp": "2026-07-03T12:00:00Z"
}
```

### GET /health

**Request:**
```
curl http://localhost:8000/health
```

**Response (200):**
```json
{
  "status": "READY",
  "registry": 25,
  "checkpoints": 25,
  "risk_rules": 25,
  "taxonomy_nodes": 233,
  "warnings": 0,
  "errors": 0
}
```

### POST /search

**Request:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "渚涘簲鍟嗚鍙瘉"}'
```

**Response (200):**
```json
{
  "total": 1,
  "checkpoints": [
    {
      "checkpoint_id": "CP-BEV-RM-001",
      "checkpoint_name": "渚涘簲鍟嗙敓浜ц鍙瘉瀹℃煡",
      "domain": "鍘熸枡绠＄悊",
      "module": "渚涘簲鍟嗙鐞?,
      "objective": "纭浼佷笟閲囪喘鐨勬墍鏈夐鍝佸師鏂欎緵搴斿晢鎸佹湁鏈夋晥鐨勯鍝佺敓浜ц鍙瘉..."
    }
  ],
  "registry_entries": [
    {
      "id": "CP-BEV-RM-001",
      "title": "渚涘簲鍟嗙敓浜ц鍙瘉瀹℃煡",
      "category": "鍘熸枡绠＄悊",
      "subcategory": "渚涘簲鍟嗚祫璐ㄥ鏍?,
      "risk_level": "High",
      "laws": ["椋熷搧鐢熶骇璁稿彲绠＄悊鍔炴硶", "椋熷搧瀹夊叏娉?],
      "evidence_required": ["渚涘簲鍟嗙敓浜ц鍙瘉澶嶅嵃浠?]
    }
  ],
  "risk_rules": [
    {
      "rule_id": "RR-CP-BEV-RM-001",
      "risk_level": "Critical",
      "condition": "璁稿彲璇佸鍗颁欢涓庡師浠朵竴鑷翠笖鍦ㄦ湁鏁堟湡鍐?
    }
  ],
  "taxonomy_nodes": [
    {"id": "raw_material_management", "name": "Raw Material Management"},
    {"id": "supplier_management", "name": "Supplier Management"},
    {"id": "supplier_qualification", "name": "Supplier Qualification"}
  ]
}
```

**Error 鈥?no criteria (422):**
```json
{
  "detail": "At least one search criterion is required (query, checkpoint_id, category, risk_level)"
}
```

### POST /inspect

**Request 鈥?search with evidence:**
```bash
curl -X POST http://localhost:8000/inspect \
  -H "Content-Type: application/json" \
  -d '{
    "query": "渚涘簲鍟嗚鍙瘉",
    "evidence": [
      {
        "id": "EV-API-001",
        "evidence_type": "OBSERVATION",
        "checkpoint_id": "CP-BEV-RM-001",
        "description": "渚涘簲鍟嗚鍙瘉榻愬叏鏈夋晥锛屽搧绉嶈寖鍥磋鐩?,
        "attachments": ["璁稿彲璇佸鍗颁欢.pdf"]
      }
    ]
  }'
```

**Response (200):**
```json
{
  "request": {
    "query": "渚涘簲鍟嗚鍙瘉",
    "checkpoint_id": "",
    "category": "",
    "risk_level": ""
  },
  "matched_checkpoints": [...],
  "matched_registry_entries": [...],
  "matched_risk_rules": [...],
  "matched_taxonomy_nodes": [...],
  "evidence": [
    {
      "id": "EV-API-001",
      "evidence_type": "OBSERVATION",
      "checkpoint_id": "CP-BEV-RM-001",
      "description": "渚涘簲鍟嗚鍙瘉榻愬叏鏈夋晥锛屽搧绉嶈寖鍥磋鐩?,
      "attachments": ["璁稿彲璇佸鍗颁欢.pdf"]
    }
  ],
  "evaluation_results": [
    {
      "checkpoint_id": "CP-BEV-RM-001",
      "rule_id": "RR-CP-BEV-RM-001",
      "evidence_id": "EV-API-001",
      "status": "PASS",
      "score": 1.0,
      "reason": "All evidence requirements satisfied",
      "violated_laws": ["椋熷搧鐢熶骇璁稿彲绠＄悊鍔炴硶", "椋熷搧瀹夊叏娉?],
      "recommendation": "渚涘簲鍟嗙敓浜ц鍙瘉瀹℃煡"
    }
  ],
  "warnings": [],
  "metadata": {
    "total_checkpoints": 1,
    "total_registry_entries": 1,
    "total_risk_rules": 1,
    "total_taxonomy_nodes": 3,
    "total_evidence": 1,
    "total_evaluation_results": 1,
    "warnings_count": 0
  }
}
```

---

## Error Handling

| Scenario | HTTP Status | Response Body |
|----------|-------------|---------------|
| No search criteria | 422 | `{"detail": "At least one search criterion is required"}` |
| Agent not initialised | 500 | `{"detail": "Agent not initialised"}` |
| Invalid evidence_type | 422 | `{"detail": "'INVALID' is not a valid EvidenceType"}` |
| Internal error | 500 | `{"detail": "Internal server error"}` |

Stack traces are never exposed to the client. Exceptions are logged server-side.

---

## Startup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start server

```bash
uvicorn api.server:app --reload
```

### Verify

```bash
curl http://localhost:8000/
# 鈫?{"name":"Food Audit Agent","version":"1.0.0","status":"running",...}
```

### Swagger UI

Open http://localhost:8000/docs in a browser.

---

## File Structure

```
api/
鈹溾攢鈹€ __init__.py        鈥?Package marker
鈹溾攢鈹€ schemas.py         鈥?Pydantic request/response models (140 lines)
鈹斺攢鈹€ server.py          鈥?FastAPI app with 4 endpoints (291 lines)
```

---

## Rules Compliance

| Rule | Status |
|------|--------|
| `knowledge/` NOT modified | 鉁?|
| `risk_rules/` NOT modified | 鉁?|
| `taxonomy/` NOT modified | 鉁?|
| `registry/` NOT modified | 鉁?|
| Core runtime logic NOT modified | 鉁?|

## Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `api/__init__.py` | 1 | Package marker |
| `api/schemas.py` | 140 | 11 Pydantic models |
| `api/server.py` | 291 | FastAPI app, 4 endpoints, lifespan, error handlers |
| `reports/api_server_report.md` | 鈥?| This report |

