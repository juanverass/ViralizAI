from fastapi import FastAPI
from app.services.service_registration_block import ServiceRegistrationBlock
from infrastructure.database import Base, engine, SessionLocal, create_database_if_not_exists
from infrastructure.repositories.repository_registration_block import RepositoryRegistrationBlock
from interfaces.api.router_registration_block import RouterRegistrationBlock

# Inicializa banco e tabelas
def init_db():
    create_database_if_not_exists()
    Base.metadata.create_all(bind=engine)
    print("Banco e tabelas estão atualizados!")

def create_app() -> FastAPI:
    app = FastAPI(title="ViralizAI 🚀")

    session = SessionLocal()
    repositories = RepositoryRegistrationBlock(session)
    services = ServiceRegistrationBlock(repositories)
    
    app.state.services = services

    routers = RouterRegistrationBlock()
    routers.register_all(app)

    return app

init_db()

app = create_app()
