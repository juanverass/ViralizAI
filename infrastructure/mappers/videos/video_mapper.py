from domain.entities.videos.video import StatusDoVideo, Video
from infrastructure.models.videos.video_model import VideoModel

class VideoMapper:
    @staticmethod
    def to_model(entity: Video) -> VideoModel:
        return VideoModel(
            id=entity.id,
            title=entity.title,
            source_url=entity.source_url,
            local_path=entity.local_path,
            status=StatusDoVideo(entity.status),
            duration=entity.duration,
            language=entity.language
        )

    @staticmethod
    def to_entity(model: VideoModel) -> Video:
        return Video(
            id=model.id,
            title=model.title,
            source_url=model.source_url,
            local_path=model.local_path,
            status=StatusDoVideo(model.status.value),
            duration=model.duration,
            language=model.language
        )