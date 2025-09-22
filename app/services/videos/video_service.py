import uuid
from domain.entities.videos.video import Video, StatusDoVideo
from infrastructure.repositories.videos.video_repository import VideoRepository

class VideoService:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    def create_video(self, title: str, source_url: str) -> Video:
        video = Video(
            id=str(uuid.uuid4()),
            title=title,
            source_url=source_url
        )
        self.repository.add(video)
        return video

    def mark_processing(self, video_id: str):
        self.repository.update_status(video_id, StatusDoVideo.PROCESSING)

    def mark_ready(self, video_id: str):
        self.repository.update_status(video_id, StatusDoVideo.READY)
