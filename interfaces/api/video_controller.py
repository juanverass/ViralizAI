from fastapi import APIRouter
from infrastructure.database import SessionLocal
from infrastructure.repositories.videos.video_repository import VideoRepository
from interfaces.api.base_controller import BaseController
from app.services.videos.video_service import VideoService
from interfaces.api.schemas.video_schemas import VideoCreateRequest, VideoUpdateRequest, VideoResponse

router = APIRouter()

# Aqui usamos BaseController passando:
# EntityType = ORM entity do vídeo (geralmente Video)
# CreateUpdateModelType = VideoUpdateRequest (ou VideoCreateRequest, depende do método)
# ResponseModelType = VideoResponse
# ServiceType = VideoService
session = SessionLocal()

video_repository = VideoRepository(session) 

video_controller = BaseController(
    router=router,
    service=VideoService(video_repository),
    response_model=VideoResponse,
    entity_name="Vídeo"
)
