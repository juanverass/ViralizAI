from infrastructure.repositories.contas.conta_repository import ContaRepository
from infrastructure.repositories.postagens_agendadas.postagem_agendada_repository import PostagemAgendadaRepository
from infrastructure.repositories.videos.video_repository import VideoRepository

class RepositoryRegistrationBlock:
    def __init__(self, session):
        self.videos = VideoRepository(session)
        self.contas = ContaRepository(session)
        self.postagens_agendadas = PostagemAgendadaRepository(session)