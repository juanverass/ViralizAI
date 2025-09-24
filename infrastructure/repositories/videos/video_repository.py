from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities.videos.video import Video, StatusDoVideo
from domain.repositories.video_repository_port import VideoRepositoryPort
from infrastructure.mappers.videos.video_mapper import VideoMapper
from infrastructure.models.videos.video_db_mapping import VideoDbMapping
from infrastructure.repositories.comuns.base_repository import BaseRepository

class VideoRepository(BaseRepository[Video, VideoDbMapping], VideoRepositoryPort):
    """Implementação do repositório de vídeos usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        super().__init__(session, VideoDbMapping, VideoMapper)
    
    def update_status(self, video_id: str, status: StatusDoVideo) -> Optional[Video]:
        """Atualiza status de um vídeo específico"""
        video = self.get_by_id(video_id)
        if video:
            video.status = status
            return self.update(video)
        return None