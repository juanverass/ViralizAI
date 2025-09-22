from infrastructure.repositories.videos.video_repository import VideoRepository

class RepositoryRegistrationBlock:
    def __init__(self, session):
        self.videos = VideoRepository(session)