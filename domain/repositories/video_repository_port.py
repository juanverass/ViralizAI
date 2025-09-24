from typing import Protocol, Optional, List
from domain.entities.videos.video import Video

class VideoRepositoryPort(Protocol):
    """Contrato para repositório de vídeos - equivalente a interface em C#"""
    
    def add(self, entity: Video) -> Video:
        """Adiciona um novo vídeo"""
        ...
    
    def get_all(self) -> List[Video]:
        """Retorna todos os vídeos"""
        ...
    
    def get_by_id(self, id_entity: str) -> Optional[Video]:
        """Busca vídeo por ID"""
        ...
    
    def update(self, entity: Video) -> Video:
        """Atualiza um vídeo existente"""
        ...
    
    def delete(self, entity: Video) -> None:
        """Remove um vídeo"""
        ...
    
    def delete_by_id(self, id_entity: str) -> None:
        """Remove vídeo por ID"""
        ...
