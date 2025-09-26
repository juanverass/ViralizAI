from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities.videos.video import Video, StatusDoVideo
from domain.repositories.video_repository_port import VideoRepositoryPort
from infrastructure.mappers.videos.video_persistence_mapper import VideoPersistenceMapper
from infrastructure.models.videos.video_db_mapping import VideoDbMapping
from infrastructure.repositories.comuns.base_repository import BaseRepository

class VideoRepository(BaseRepository[Video, VideoDbMapping], VideoRepositoryPort):
    """Implementação do repositório de vídeos usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        super().__init__(session, VideoDbMapping, VideoPersistenceMapper)