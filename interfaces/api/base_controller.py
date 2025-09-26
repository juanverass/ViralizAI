from typing import Generic, TypeVar, Type, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.base_app_service import BaseAppService

# Tipos genéricos
EntityType = TypeVar("EntityType")  # Entidade de domínio ou ORM
CreateUpdateModelType = TypeVar("CreateUpdateModelType", bound=BaseModel)  # Pydantic para criação/atualização
ResponseModelType = TypeVar("ResponseModelType", bound=BaseModel)  # Pydantic para resposta
ServiceType = TypeVar("ServiceType", bound=BaseAppService)

class BaseController(Generic[EntityType, CreateUpdateModelType, ResponseModelType, ServiceType]):
    """Controller base com operações CRUD padrão"""

    def __init__(
        self,
        router: APIRouter,
        service: ServiceType,
        response_model: Type[ResponseModelType],
        entity_name: str
    ):
        self.router = router
        self.service = service
        self.response_model = response_model
        self.entity_name = entity_name
        self._register_routes()

    def _register_routes(self):
        """Registra as rotas padrão do CRUD"""

        @self.router.get("/", response_model=List[self.response_model])
        def list_entities():
            """Lista todas as entidades"""
            entities = self.service.get_all()
            return [self._to_response_model(e) for e in entities]

        @self.router.get("/{entity_id}", response_model=self.response_model)
        def get_entity(entity_id: str):
            """Busca entidade por ID"""
            entity = self.service.get_by_id(entity_id)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.entity_name} não encontrado"
                )
            return self._to_response_model(entity)

        @self.router.put("/{entity_id}", response_model=self.response_model)
        def update_entity(entity_id: str, entity_data: CreateUpdateModelType):
            """Atualiza uma entidade"""
            entity = self.service.get_by_id(entity_id)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.entity_name} não encontrado"
                )

            # Atualiza apenas campos enviados
            for key, value in entity_data.model_dump(exclude_unset=True).items():
                if hasattr(entity, key):
                    setattr(entity, key, value)

            updated_entity = self.service.update(entity)
            return self._to_response_model(updated_entity)

        @self.router.delete("/{entity_id}")
        def delete_entity(entity_id: str):
            """Remove uma entidade por ID"""
            entity = self.service.get_by_id(entity_id)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.entity_name} não encontrado"
                )
            self.service.delete_by_id(entity_id)
            return {"message": f"{self.entity_name} removido com sucesso"}

    def _to_response_model(self, entity: EntityType) -> ResponseModelType:
        """
        Converte qualquer entidade para o Pydantic ResponseModel
        Compatível com Pydantic v2 (model_validate)
        """
        # Se a entidade já for um dict, valida direto
        if isinstance(entity, dict):
            return self.response_model.model_validate(entity)

        # Se a entidade for um ORM ou domain object, converte com vars()
        return self.response_model.model_validate(vars(entity))
