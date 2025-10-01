from app.services.base_app_service import BaseAppService
from domain.entities.postagens_agendadas.postagem_agendada import PostagemAgendada
from domain.repositories.postagem_agendada_repository_port import PostagemAgendadaRepositoryPort as _repository


class PostagemAgendadaService(BaseAppService[PostagemAgendada]):
    """Serviço de postagens agendadas - casos de uso específicos do domínio"""

    def __init__(self, repository: _repository):
        super().__init__(repository)