from domain.entities.videos.video import Video, StatusDoVideo
from infrastructure.mappers.videos.video_mapper import VideoMapper
from infrastructure.models.videos.video_model import VideoModel
from infrastructure.repositories.comuns.base_repository import BaseRepository

class VideoRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, VideoModel, VideoMapper)