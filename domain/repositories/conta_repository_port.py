from domain.entities.contas.conta import Conta
from domain.repositories.base_repository_port import BaseRepositoryPort

class ContaRepositoryPort(BaseRepositoryPort[Conta]):
    """Contrato para repositório de contas"""