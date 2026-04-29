# mappers/patient.py
from engine.registry import register
from db.connection import QueryRunner


class PatientMapper:
    resource_type = "Patient"

    _QUERY = """
        SELECT
            id,
            nome,
            cpf,
            data_nascimento,
            sexo,
            telefone
        FROM pessoas
        WHERE id = %s
          AND tipo_pessoa = 'PAC'
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

        return {
            "resourceType": "Patient",
            "id": str(row["id"]),
            "identifier": [
                {
                    "system": "urn:oid:2.16.840.1.113883.13.236",  # OID CPF Brasil
                    "value": row["cpf"],
                }
            ] if row["cpf"] else [],
            "name": [
                {
                    "use": "official",
                    "text": row["nome"],
                    "family": family,
                    "given": [given],
                }
            ],
            "gender": self._GENDER.get(row["sexo"], "unknown"),
            "birthDate": self._to_fhir_date(row["data_nascimento"]),
            "telecom": [
                {
                    "system": "phone",
                    "value": row["telefone"],
                    "use": "home",
                }
            ] if row["telefone"] else [],
        }

    def _split_name(self, nome: str) -> tuple[str, str]:
        """Separa o nome completo em given (primeiros nomes) e family (último sobrenome)."""
        parts = nome.strip().split()
        if len(parts) == 1:
            return parts[0], ""
        return " ".join(parts[:-1]), parts[-1]

    def _to_fhir_date(self, value) -> str | None:
        """Converte date/datetime do postgres para string YYYY-MM-DD."""
        if not value:
            return None
        return value.isoformat()[:10]


register(PatientMapper())