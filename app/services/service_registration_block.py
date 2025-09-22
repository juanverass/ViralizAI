from app.services.videos.video_service import VideoService


class ServiceRegistrationBlock:
    def __init__(self, repositorys):
        self.video_service = VideoService(repositorys.videos)