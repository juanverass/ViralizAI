from typing import Optional
from domain.entities.videos.video import Video, StatusDoVideo
from domain.repositories.video_repository_port import VideoRepositoryPort as _repository
from app.services.base_app_service import BaseAppService
from infrastructure.external.veo3.veo3_service import Veo3Service

class VideoService(BaseAppService[Video]):
    """Serviço de vídeos - casos de uso específicos do domínio"""
    
    def __init__(self, repository: _repository):
        super().__init__(repository)

    def create_video(self, title: str, source_url: str) -> Video:
        """Cria um novo vídeo"""
        video = Video.create_new(title, source_url)
        return  _repository.add(video)
    
    def create_video_by_roteiro(self, roteiro: str) -> dict:
        """
        Cria um vídeo via PiAPI Kling usando o roteiro informado.
        """
        resultado = Veo3Service.gerar_video_VEO3(roteiro)
        return resultado    
