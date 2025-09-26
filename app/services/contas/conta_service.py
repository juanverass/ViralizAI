from typing import Optional
from domain.entities.contas.conta import Conta
from domain.repositories.conta_repository_port import ContaRepositoryPort as _repository
from app.services.base_app_service import BaseAppService

class ContaService(BaseAppService[Conta]):
    """Serviço de vídeos - casos de uso específicos do domínio"""
    
    def __init__(self, repository: _repository):
        super().__init__(repository)