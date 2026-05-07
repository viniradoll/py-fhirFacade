from fastapi import APIRouter, Depends, HTTPException
from db.connection import QueryRunner, get_db
from engine.registry import resolve
from datetime import date

router = APIRouter(prefix="/fhir")

def get_query_runner(conn=Depends(get_db)) -> QueryRunner:
    return QueryRunner(conn)

@router.get("/{resource_type}/{id}")
def get_resource(
    resource_type: str,
    id: int,
    db: QueryRunner = Depends(get_query_runner),
) -> dict:
    try:
        mapper = resolve(resource_type)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Recurso '{resource_type}' não suportado. "
                   f"Consulte /fhir/metadata para recursos disponíveis.",
        )

    result = mapper.map(id, db)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"{resource_type} com id '{id}' não encontrado.",
        )

    return result

@router.get("/metadata")
def capability_statement() -> dict:
    from engine.registry import registered_resources

    return {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "kind": "instance",
        "date": date.today(),
        "format": ["json"],
        "fhirVersion": "4.0.1",
        "implementation": {
            "description": "FHIR Facade over legacy laboratory database",
            "url": "localhost:8000",
        },
        "rest": [{
            "mode": "server",
            "resource": [
                {"type": r, "interaction": [{"code": "read"}]}
                for r in registered_resources()
            ],
        }],
    }