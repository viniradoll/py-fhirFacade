from engine.registry import register
from db.connection import QueryRunner


class EncounterMapper:
    resource_type = "Encounter"

    _QUERY = """
        SELECT
            a.id,
            a.data_atendimento,
            a.tipo_atendimento,
            a.status,
            a.observacoes,
            a.paciente_id,
            a.medico_id,
            a.operadora_id,
            o.nome        AS operadora_nome,
            o.plano_nome  AS operadora_plano
        FROM atendimentos a
        LEFT JOIN operadoras o ON o.id = a.operadora_id
        WHERE a.id = %s
    """

    _STATUS = {
        "FINALIZADO":  "finished",
        "EM ANDAMENTO": "in-progress",
        "CANCELADO":   "cancelled",
        "AGENDADO":    "planned",
    }

    def map(self, id: int, db: QueryRunner) -> dict | None:
        row = db.fetch_one(self._QUERY, (id,))
        if not row:
            return None

        resource = {
            "resourceType": "Encounter",
            "id": str(row["id"]),
            "status": self._STATUS.get(row["status"], "unknown"),
            "class": {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "AMB",
                "display": "ambulatory",
            },
            "type": [
                {
                    "text": row["tipo_atendimento"],
                }
            ],
            "subject": {
                "reference": f"Patient/{row['paciente_id']}",
            },
            "participant": [
                {
                    "individual": {
                        "reference": f"Practitioner/{row['medico_id']}",
                    }
                }
            ],
            "period": {
                "start": self._to_fhir_datetime(row["data_atendimento"]),
            },
        }

        if row["observacoes"]:
            resource["reasonCode"] = [{"text": row["observacoes"]}]

        if row["operadora_id"]:
            resource["serviceProvider"] = {
                "display": f"{row['operadora_nome']} — {row['operadora_plano']}",
            }

        return resource

    def _to_fhir_datetime(self, value) -> str | None:
        if not value:
            return None
        return value.isoformat()


register(EncounterMapper())