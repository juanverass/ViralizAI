from fastapi import FastAPI
from app.services.service_registration_block import ServiceRegistrationBlock
from infrastructure.database import Base, engine, SessionLocal, create_database_if_not_exists
from infrastructure.mappers.videos.video_persistence_mapper import VideoPersistenceMapper
from infrastructure.models.videos.video_db_mapping import VideoDbMapping
from infrastructure.repositories.repository_registration_block import RepositoryRegistrationBlock
from interfaces.api.router_registration_block import RouterRegistrationBlock

# Inicializa banco e tabelas
def init_db():
    create_database_if_not_exists()
    Base.metadata.create_all(bind=engine)
    print("Banco e tabelas estão atualizados!")

def create_app() -> FastAPI:
    app = FastAPI(title="ViralizAI 🚀")

    # Criação da sessão do banco
    session = SessionLocal()

    # Registro dos repositórios (implementações concretas)
    repositories = RepositoryRegistrationBlock(session)
    
    # Registro dos serviços (casos de uso) - recebem os repositórios via Protocol
    services = ServiceRegistrationBlock(repositories)
    
    # Injeção dos serviços no estado da aplicação
    app.state.services = services

    # Registro das rotas da API
    routers = RouterRegistrationBlock()
    routers.register_all(app)

    return app

init_db()

app = create_app()
