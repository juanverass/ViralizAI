from domain.entities.postagens_agendadas.postagem_agendada import PostagemAgendada
from domain.repositories.postagem_agendada_repository_port import PostagemAgendadaRepositoryPort
from sqlalchemy.orm import Session
from infrastructure.mappers.postagens_agendadas.postagem_agendada_persistence_mapper import PostagemAgendadaPersistenceMapper
from infrastructure.models.postagens_agendadas.postagem_agendada_db_mapping import PostagemAgendadaDbMapping
from infrastructure.repositories.comuns.base_repository import BaseRepository

class PostagemAgendadaRepository(BaseRepository[PostagemAgendada, PostagemAgendadaDbMapping], PostagemAgendadaRepositoryPort):
    def __init__(self, session: Session):
        super().__init__(session, PostagemAgendadaDbMapping, PostagemAgendadaPersistenceMapper)