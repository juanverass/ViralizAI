from domain.entities.postagens_agendadas.postagem_agendada import PostagemAgendada
from domain.repositories.base_repository_port import BaseRepositoryPort


class PostagemAgendadaRepositoryPort(BaseRepositoryPort[PostagemAgendada]):
    """Contrato para repositório de Postagens Agendadas"""
