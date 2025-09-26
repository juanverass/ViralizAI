from fastapi import APIRouter
from app.services.contas.conta_service import ContaService
from infrastructure.database import SessionLocal
from infrastructure.repositories.contas.conta_repository import ContaRepository
from infrastructure.repositories.videos.video_repository import VideoRepository
from interfaces.api.base_controller import BaseController
from interfaces.api.schemas.conta_schemas import ContaResponse

router = APIRouter()
session = SessionLocal()
conta_repository = ContaRepository(session) 
conta_service = ContaService(conta_repository)
conta_controller = BaseController(
    router=router,
    service= conta_service,
    response_model=ContaResponse,
    entity_name="Conta"
)