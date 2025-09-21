from infrastructure.database import Base, engine, SessionLocal, create_database_if_not_exists
from infrastructure.models.videos.video_model import VideoModel
from infrastructure.repositories.videos.video_repository import VideoRepository
from app.services.videos.video_service import VideoService
from domain.entities.videos.video import VideoStatus

def init_db():
    """Garante banco e tabelas existentes"""
    create_database_if_not_exists()
    Base.metadata.create_all(bind=engine)
    print("Banco e tabelas prontos!")

def run_app():
    """Fluxo principal da aplicação"""
    # Inicializa sessão e repositório
    session = SessionLocal()
    repo = VideoRepository(session)
    service = VideoService(repo)

    # Cria vídeo de teste
    video = service.create_video("Meu Primeiro Vídeo", "https://youtu.be/exemplo")
    print(f"[CRIADO] Vídeo: {video.id} - {video.title} - Status: {video.status.value}")

    # Atualiza status para PROCESSING
    service.mark_processing(video.id)
    updated_video = repo.get_by_id(video.id)
    print(f"[ATUALIZADO] Vídeo: {updated_video.id} - Status: {updated_video.status.value}")

    # Aqui você pode adicionar chamadas a dublagem, legenda, geração de vídeo etc.

    session.close()

if __name__ == "__main__":
    init_db()
    run_app()