from engine.registry import register
from db.connection import QueryRunner


class PractitionerMapper:
    resource_type = "Practitioner"

    _QUERY = """
        SELECT
            id,
            nome,
            cpf,
            sexo,
            data_nascimento,
            registro_profissional,
            especialidade,
            telefone
        FROM pessoas
        WHERE id = %s
          AND tipo_pessoa = 'MED'
    """

    _GENDER = {
        "M": "male",
        "F": "female",
    }

    def map(self, id: int, db: QueryRunner) -> dict | None:
        row = db.fetch_one(self._QUERY, (id,))
        if not row:
            return None

        given, family = self._split_name(row["nome"])

        resource = {
            "resourceType": "Practitioner",
            "id": str(row["id"]),
            "name": [
                {
                    "use": "official",
                    "text": row["nome"],
                    "family": family,
                    "given": [given],
                }
            ],
            "gender": self._GENDER.get(row["sexo"], "unknown"),
        }

        if row["cpf"]:
            resource["identifier"] = [
                {
                    "system": "urn:oid:2.16.840.1.113883.13.236",
                    "value": row["cpf"],
                }
            ]

        if row["registro_profissional"]:
            resource.setdefault("identifier", []).append(
                {
                    "system": "http://www.portalcrm.cfm.org.br",
                    "value": row["registro_profissional"],
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "MD",
                                "display": "Medical License Number",
                            }
                        ]
                    },
                }
            )

        if row["especialidade"]:
            resource["qualification"] = [
                {
                    "code": {
                        "text": row["especialidade"],
                    }
                }
            ]

        if row["telefone"]:
            resource["telecom"] = [
                {
                    "system": "phone",
                    "value": row["telefone"],
                }
            ]

        if row["data_nascimento"]:
            resource["birthDate"] = row["data_nascimento"].isoformat()

        return resource

    def _split_name(self, nome: str) -> tuple[str, str]:
        parts = nome.strip().split()
        if len(parts) == 1:
            return parts[0], ""
        return " ".join(parts[:-1]), parts[-1]


register(PractitionerMapper())