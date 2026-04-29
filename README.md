# FHIR Facade

A read-only FHIR R4 facade over a legacy PostgreSQL laboratory database, built with FastAPI and modern Python. Exposes clinical data as standard HL7 FHIR resources without modifying the underlying system.

---

## Overview

This project implements an interoperability layer that wraps a non-normalized legacy database and exposes its data through a RESTful FHIR R4 API. The architecture follows the **Strangler Fig** pattern — the legacy system is preserved untouched while a standards-compliant interface is built around it.

The server is intentionally **read-only**, reflecting both the complexity of writing to a denormalized schema and the principle that a facade should expose data, not own it.

---

## Supported Resources

| FHIR Resource | Source Table | Description |
|---|---|---|
| `Patient` | `pessoas` (PAC) | Laboratory patients |
| `Practitioner` | `pessoas` (MED) | Requesting physicians |
| `Encounter` | `atendimentos` | Laboratory visits |
| `Condition` | `condicoes` | Diagnoses with ICD-10 coding |
| `Organization` | `operadoras` | Health insurance providers |

Capability statement available at `GET /fhir/metadata`.

---

## Architecture

```
fhir_facade/
├── main.py               # FastAPI app + lifespan
├── config.py             # Singleton settings via pydantic-settings
├── db/
│   └── connection.py     # Connection pool + QueryRunner abstraction
├── engine/
│   ├── base.py           # FHIRMapper Protocol (structural contract)
│   ├── registry.py       # Global mapper registry
│   └── loader.py         # Auto-discovery via importlib
├── mappers/
│   ├── patient.py
│   ├── practitioner.py
│   ├── encounter.py
│   ├── condition.py
│   └── organization.py
└── routers/
    └── fhir.py           # Single generic FHIR endpoint
```

### Key Design Decisions

**Protocol over ABC** — Mappers satisfy the `FHIRMapper` contract structurally (PEP 544), with no inheritance required. Concrete mappers have zero coupling to the engine layer.

**Convention over Configuration** — Dropping a new file into `mappers/` is sufficient to register a new resource. The loader discovers and imports all mappers at startup via `importlib`.

**Single generic endpoint** — `GET /fhir/{resource_type}/{id}` serves all resources. The router resolves the correct mapper from the registry at request time.

**QueryRunner abstraction** — Mappers never touch the database driver directly. They receive a `QueryRunner` instance that exposes only `fetch_one()` and `fetch_many()`, keeping mappers fully decoupled from psycopg internals.

---

## API Endpoints

```
GET /fhir/metadata              # CapabilityStatement
GET /fhir/Patient/{id}
GET /fhir/Practitioner/{id}
GET /fhir/Encounter/{id}
GET /fhir/Condition/{id}
GET /fhir/Organization/{id}
```

Resource types are **case-sensitive** per the FHIR R4 specification. Requests with incorrect casing return a `404` with a correction suggestion.

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) or pip

### Installation

```bash
git clone https://github.com/viniradoll/py-fhirFacade.git
cd py-fhirFacade

pip install -r requirements.txt
```

### Docker

```bash
docker compose up
```

---

## Adding a New Resource

1. Create `mappers/your_resource.py` with a class that implements `resource_type` and `map()`
2. Call `register(YourResourceMapper())` at the bottom of the file
3. Restart the server (or rely on `--reload` in development)

No other files need to be modified.

```python
# mappers/your_resource.py
from engine.registry import register
from db.connection import QueryRunner

class YourResourceMapper:
    resource_type = "YourResource"

    _QUERY = "SELECT * FROM your_table WHERE id = %s"

    def map(self, id: int, db: QueryRunner) -> dict | None:
        row = db.fetch_one(self._QUERY, (id,))
        if not row:
            return None
        return {
            "resourceType": "YourResource",
            "id": str(row["id"]),
            # ...
        }

register(YourResourceMapper())
```

---

## Requirements

```
fastapi
uvicorn
psycopg[binary]
psycopg-pool
pydantic-settings
```

---

## FHIR Compliance Notes

- Implements **HL7 FHIR R4**
- Server capabilities declared via `CapabilityStatement` at `/fhir/metadata`
- CPF identifier uses OID `2.16.840.1.113883.13.236` (official Brazilian HL7 identifier)
- CRM identifier uses system `http://www.portalcrm.cfm.org.br` with type code `MD`
- ICD-10 codes use system `http://hl7.org/fhir/sid/icd-10`
- Resource types enforce PascalCase per specification

---

## License

MIT
