from app.services.videos.video_service import VideoService
from infrastructure.repositories.repository_registration_block import RepositoryRegistrationBlock


class ServiceRegistrationBlock:
    def __init__(self, repositories: RepositoryRegistrationBlock):
        self.video_service = VideoService(repositories.videos)