from typing import Optional
from domain.entities.videos.video import Video, StatusDoVideo
from domain.repositories.video_repository_port import _repository
from app.services.base_app_service import BaseAppService

class VideoService(BaseAppService[Video]):
    """Serviço de vídeos - casos de uso específicos do domínio"""
    
    def __init__(self, repository: _repository):
        super().__init__(repository)

    def create_video(self, title: str, source_url: str) -> Video:
        """Cria um novo vídeo"""
        video = Video.create_new(title, source_url)
        return  _repository.add(video)
     
