from domain.entities.videos.video import Video
from infrastructure.models.videos.video_model import VideoModel, VideoStatusEnum

class VideoRepository:
    ...

    def add(self, video: Video):
        model = VideoModel(
            id=video.id,  # UUID em string
            title=video.title,
            source_url=video.source_url,
            local_path=video.local_path,
            status=VideoStatusEnum(video.status.value),
            duration=video.duration,
            language=video.language
        )
        self.session.add(model)
        self.session.commit()