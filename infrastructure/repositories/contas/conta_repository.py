

from domain.entities.contas.conta import Conta
from sqlalchemy.orm import Session
from domain.repositories.conta_repository_port import ContaRepositoryPort
from infrastructure.mappers.contas.conta_mapper import ContaPercistenceMapper
from infrastructure.models.contas.conta_db_mapping import ContaDbMapping
from infrastructure.repositories.comuns.base_repository import BaseRepository


class ContaRepository(BaseRepository[Conta, ContaDbMapping], ContaRepositoryPort):
    """Implementação do repositório de vídeos usando SQLAlchemy"""

    def __init__(self, session: Session):
        super().__init__(session, ContaDbMapping, ContaPercistenceMapper)