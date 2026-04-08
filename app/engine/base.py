from typing import Protocol
from db.connection import QueryRunner

class FHIRMapper(Protocol):
    resource_type: str

    def map(self, id: int, db: QueryRunner) -> dict: ...