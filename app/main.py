from app.services.service_registration_block import ServiceRegistrationBlock
from infrastructure.database import Base, engine, SessionLocal, create_database_if_not_exists
from infrastructure.models.videos.video_model import VideoModel
from infrastructure.repositories.repository_registration_block import RepositoryRegistrationBlock
from infrastructure.repositories.videos.video_repository import VideoRepository
from app.services.videos.video_service import VideoService

def init_db():
    """Garante banco e tabelas existentes"""
    create_database_if_not_exists()
    Base.metadata.create_all(bind=engine)
    print("Banco e tabelas prontos!")

def run_app():
    """Fluxo principal da aplicação"""
    # Inicializa sessão e repositório
    session = SessionLocal()
    repositorys = RepositoryRegistrationBlock(session)
    services = ServiceRegistrationBlock(repositorys)

    # Cria vídeo de teste
    video = services.video_service.create_video("Meu Primeiro Vídeo", "https://youtu.be/exemplo")
    print(f"[CRIADO] Vídeo: {video.id} - {video.title} - Status: {video.status.value}")

    session.close()

if __name__ == "__main__":
    init_db()
    run_app()