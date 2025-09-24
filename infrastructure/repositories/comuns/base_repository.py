from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# TypeVar para entidade e model genéricos
EntityType = TypeVar('EntityType')
ModelType = TypeVar('ModelType')

class BaseRepository(Generic[EntityType, ModelType]):
    """Repositório base genérico com operações CRUD completas"""
    
    def __init__(self, session: Session, model: Type[ModelType], mapper):
        self.session = session
        self.model = model
        self.mapper = mapper

    def add(self, entity: EntityType) -> EntityType:
        """Adiciona uma nova entidade"""
        model_instance = self.mapper.to_model(entity)
        self.session.add(model_instance)
        self.session.commit()
        self.session.refresh(model_instance)
        return self.mapper.to_entity(model_instance)

    def get_all(self) -> List[EntityType]:
        """Retorna todas as entidades"""
        results = self.session.query(self.model).all()
        return [self.mapper.to_entity(item) for item in results]

    def get_by_id(self, id_entity: str) -> Optional[EntityType]:
        """Busca entidade por ID"""
        model_instance = self.session.query(self.model).filter_by(id=id_entity).first()
        return self.mapper.to_entity(model_instance) if model_instance else None

    def update(self, entity: EntityType) -> EntityType:
        """Atualiza uma entidade existente"""
        model_instance = self.mapper.to_model(entity)
        self.session.merge(model_instance)
        self.session.commit()
        self.session.refresh(model_instance)
        return self.mapper.to_entity(model_instance)

    def delete(self, entity: EntityType) -> None:
        """Remove uma entidade"""
        model_instance = self.mapper.to_model(entity)
        self.session.delete(model_instance)
        self.session.commit()

    def delete_by_id(self, id_entity: str) -> None:
        """Remove entidade por ID"""
        self.session.query(self.model).filter_by(id=id_entity).delete()
        self.session.commit()

    def find_by(self, **filters) -> List[EntityType]:
        """Busca entidades por filtros (kwargs)"""
        results = self.session.query(self.model).filter_by(**filters).all()
        return [self.mapper.to_entity(item) for item in results]

    def find_one_by(self, **filters) -> Optional[EntityType]:
        """Busca uma entidade por filtros (kwargs)"""
        model_instance = self.session.query(self.model).filter_by(**filters).first()
        return self.mapper.to_entity(model_instance) if model_instance else None

    def count(self) -> int:
        """Conta total de entidades"""
        return self.session.query(self.model).count()

    def exists(self, id_entity: str) -> bool:
        """Verifica se entidade existe por ID"""
        return self.session.query(self.model).filter_by(id=id_entity).first() is not None

    def query(self):
        """Retorna query builder para consultas customizadas"""
        return self.session.query(self.model)