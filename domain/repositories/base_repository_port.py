from typing import Protocol, TypeVar, Generic, Optional, List

EntityType = TypeVar('EntityType')


class RepositoryPort(Protocol, Generic[EntityType]):
    """Contrato genérico para repositórios do domínio"""

    def add(self, entity: EntityType) -> EntityType: ...

    def get_all(self) -> List[EntityType]: ...

    def get_by_id(self, id_entity: str) -> Optional[EntityType]: ...

    def update(self, entity: EntityType) -> EntityType: ...

    def delete(self, entity: EntityType) -> None: ...

    def delete_by_id(self, id_entity: str) -> None: ...

