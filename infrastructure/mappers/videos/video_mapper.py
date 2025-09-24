from domain.entities.videos.video import StatusDoVideo, Video
from infrastructure.models.videos.video_db_mapping import VideoDbMapping

class VideoMapper:
    @staticmethod
    def to_model(entity: Video) -> VideoDbMapping:
        return VideoDbMapping(
            id=entity.id,
            title=entity.title,
            source_url=entity.source_url,
            local_path=entity.local_path,
            status=entity.status,
            duration=entity.duration,
            language=entity.language
        )

    @staticmethod
    def to_entity(model: VideoDbMapping) -> Video:
        return Video(
            id=model.id,
            title=model.title,
            source_url=model.source_url,
            local_path=model.local_path,
            status=StatusDoVideo(model.status.value),
            duration=model.duration,
            language=model.language
        )