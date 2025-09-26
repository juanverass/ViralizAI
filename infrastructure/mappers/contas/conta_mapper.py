from domain.entities.contas.conta import Conta
from infrastructure.models.contas.conta_db_mapping import ContaDbMapping


class ContaPercistenceMapper:
    @staticmethod
    def to_model(entity: Conta) -> ContaDbMapping:
        return ContaDbMapping(
            Id = entity.Id,
            Nome = entity.Nome,
            Plataforma = entity.Plataforma.value,
            DataDeCadastro = entity.DataDeCadastro
        )
    
    
    @staticmethod
    def to_entity(model: ContaDbMapping) -> Conta:
        return Conta(
            Id = model.Id,
            Nome = model.Nome,
            Plataforma = model.Plataforma.value,
            DataDeCadastro = model.DataDeCadastro
        )