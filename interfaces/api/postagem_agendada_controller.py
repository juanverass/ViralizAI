from fastapi import APIRouter
from app.services.postagens_agendadas.postagem_agendada_service import PostagemAgendadaService
from infrastructure.database import SessionLocal
from infrastructure.repositories.postagens_agendadas.postagem_agendada_repository import PostagemAgendadaRepository
from interfaces.api.base_controller import BaseController
from interfaces.api.schemas.postagem_agendada_schemas import PostagemAgendadaResponse

router = APIRouter()
session = SessionLocal()
postagem_agendada_repository = PostagemAgendadaRepository(session) 
postagem_agendada_service = PostagemAgendadaService(postagem_agendada_repository)
conta_controller = BaseController(
    router=router,
    service= postagem_agendada_service,
    response_model=PostagemAgendadaResponse,
    entity_name="PostagemAgendada"
)