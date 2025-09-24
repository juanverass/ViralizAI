from typing import Generic, TypeVar, List, Optional
from domain.repositories.base_repository_port import RepositoryPort

EntityType = TypeVar('EntityType')


class BaseAppService(Generic[EntityType]):
    """Service base com operações CRUD padronizadas para casos de uso comuns."""

    def __init__(self, repository: RepositoryPort[EntityType]):
        self._repository = repository

    # Create
    def add(self, entity: EntityType) -> EntityType:
        return self._repository.add(entity)

    # Read
    def get_all(self) -> List[EntityType]:
        return self._repository.get_all()

    def get_by_id(self, entity_id: str) -> Optional[EntityType]:
        return self._repository.get_by_id(entity_id)

    # Update
    def update(self, entity: EntityType) -> EntityType:
        return self._repository.update(entity)

    # Delete
    def delete(self, entity: EntityType) -> None:
        self._repository.delete(entity)

    def delete_by_id(self, entity_id: str) -> None:
        self._repository.delete_by_id(entity_id)


