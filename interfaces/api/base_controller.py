from typing import Generic, TypeVar, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.services.base_app_service import BaseAppService

EntityType = TypeVar('EntityType')
ServiceType = TypeVar('ServiceType', bound=BaseAppService)

class BaseController(Generic[EntityType, ServiceType]):
    """Controller base com operações CRUD padrão"""
    
    def __init__(self, router: APIRouter, service: ServiceType, entity_name: str):
        self.router = router
        self.service = service
        self.entity_name = entity_name
        self._register_routes()
    
    def _register_routes(self):
        """Registra as rotas padrão do CRUD"""
        
        @self.router.get("", response_model=List[Any])
        def get_all():
            """Lista todas as entidades"""
            return self.service.get_all()
        
        @self.router.get("/{entity_id}")
        def get_by_id(entity_id: str):
            """Busca entidade por ID"""
            entity = self.service.get_by_id(entity_id)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.entity_name} não encontrado"
                )
            return entity
        
        @self.router.put("/{entity_id}")
        def update(entity_id: str, entity_data: dict):
            """Atualiza uma entidade"""
            entity = self.service.get_by_id(entity_id)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.entity_name} não encontrado"
                )
            
            # Atualiza os campos fornecidos
            for key, value in entity_data.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            
            return self.service.update(entity)
        
        @self.router.delete("/{entity_id}")
        def delete(entity_id: str):
            """Remove uma entidade por ID"""
            entity = self.service.get_by_id(entity_id)
            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.entity_name} não encontrado"
                )
            
            self.service.delete_by_id(entity_id)
            return {"message": f"{self.entity_name} removido com sucesso"}
