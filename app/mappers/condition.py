from engine.registry import register
from db.connection import QueryRunner


class ConditionMapper:
    resource_type = "Condition"

    _QUERY = """
        SELECT
            c.id,
            c.descricao,
            c.codigo_cid,
            c.data_diagnostico,
            c.status,
            c.paciente_id,
            c.atendimento_id
        FROM condicoes c
        WHERE c.id = %s
    """

    # Mapeamento de status legado para FHIR Clinical Status
    _CLINICAL_STATUS = {
        "ativa":     "active",
        "resolvida": "resolved",
        "inativa":   "inactive",
        "recidiva":  "recurrence",
    }

    def map(self, id: int, db: QueryRunner) -> dict | None:
        row = db.fetch_one(self._QUERY, (id,))
        if not row:
            return None

        resource = {
            "resourceType": "Condition",
            "id": str(row["id"]),
            "clinicalStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                        "code": self._CLINICAL_STATUS.get(
                            (row["status"] or "").lower(), "unknown"
                        ),
                    }
                ]
            },
            "subject": {
                "reference": f"Patient/{row['paciente_id']}",
            },
        }

        if row["codigo_cid"]:
            resource["code"] = {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/sid/icd-10",
                        "code": row["codigo_cid"],
                        "display": row["descricao"],
                    }
                ],
                "text": row["descricao"],
            }
        elif row["descricao"]:
            resource["code"] = {"text": row["descricao"]}

        if row["data_diagnostico"]:
            resource["onsetDateTime"] = row["data_diagnostico"].isoformat()

        if row["atendimento_id"]:
            resource["encounter"] = {
                "reference": f"Encounter/{row['atendimento_id']}",
            }

        return resource


register(ConditionMapper())