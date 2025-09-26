from domain.entities.contas.conta import Conta
from infrastructure.models.contas.conta_db_mapping import ContaDbMapping


class ContaMapper:
    @staticmethod
    def to_model(entity: Conta) -> ContaDbMapping:
        Id=entity.Id
        