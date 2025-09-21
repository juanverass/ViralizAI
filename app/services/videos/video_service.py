import uuid
from domain.entities.videos.video import Video, VideoStatus
from infrastructure.repositories.videos.video_repository import VideoRepository

class VideoService:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    def create_video(self, title: str, source_url: str) -> Video:
        """Cria um novo vídeo e salva no banco"""
        video = Video(
            id=str(uuid.uuid4()),  # gera UUID automaticamente
            title=title,
            source_url=source_url
        )
        self.repository.add(video)
        return video

    def mark_processing(self, video_id: str):
        """Atualiza o status do vídeo para PROCESSING"""
        self.repository.update_status(video_id, VideoStatus.PROCESSING)

    def mark_ready(self, video_id: str):
        """Atualiza o status do vídeo para READY"""
        self.repository.update_status(video_id, VideoStatus.READY)
