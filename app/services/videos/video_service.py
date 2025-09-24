from typing import Optional
from domain.entities.videos.video import Video, StatusDoVideo
from domain.repositories.video_repository_port import VideoRepositoryPort
from app.services.base_app_service import BaseAppService

class VideoService(BaseAppService[Video]):
    """Serviço de vídeos - casos de uso específicos do domínio"""
    
    def __init__(self, repository: VideoRepositoryPort):
        super().__init__(repository)

    def create_video(self, title: str, source_url: str) -> Video:
        """Cria um novo vídeo"""
        video = Video.create_new(title, source_url)
        return self.add(video)

    def mark_processing(self, video_id: str) -> Optional[Video]:
        """Marca vídeo como processando"""
        return self._repository.update_status(video_id, StatusDoVideo.PROCESSING)

    def mark_ready(self, video_id: str) -> Optional[Video]:
        """Marca vídeo como pronto"""
        return self._repository.update_status(video_id, StatusDoVideo.READY)

    def mark_failed(self, video_id: str) -> Optional[Video]:
        """Marca vídeo como falhou"""
        return self._repository.update_status(video_id, StatusDoVideo.FAILED)
