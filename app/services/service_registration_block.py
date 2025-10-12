from app.services.contas.conta_service import ContaService
from app.services.postagens_agendadas.postagem_agendada_service import PostagemAgendadaService
from app.services.videos.video_service import VideoService
from infrastructure.repositories.repository_registration_block import RepositoryRegistrationBlock
from infrastructure.external.veo3.veo3_service import Veo3Service


class ServiceRegistrationBlock:
    def __init__(self, repositories: RepositoryRegistrationBlock):
        self.video_service = VideoService(repositories.videos)
        self.conta_service = ContaService(repositories.contas)
        self.postagem_agendada_service = PostagemAgendadaService(repositories.postagens_agendadas)
        self.veo3_service = Veo3Service()