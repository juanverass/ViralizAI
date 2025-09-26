from typing import Protocol, Optional, List
from domain.entities.videos.video import Video
from domain.repositories.base_repository_port import BaseRepositoryPort

class VideoRepositoryPort(BaseRepositoryPort[Video]):
    """Contrato para repositório de vídeos"""     
