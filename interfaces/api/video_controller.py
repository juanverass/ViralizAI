from fastapi import APIRouter, Depends, Request, HTTPException, status
from typing import List
from app.services.service_registration_block import ServiceRegistrationBlock
from app.services.videos.video_service import VideoService
from interfaces.api.schemas.video_schemas import VideoCreateRequest, VideoUpdateRequest, VideoResponse
from domain.entities.videos.video import Video
from interfaces.api.base_controller import BaseController

router = APIRouter()

def get_services(request: Request) -> ServiceRegistrationBlock:
    return request.app.state.services

def get_video_service(services: ServiceRegistrationBlock = Depends(get_services)) -> VideoService:
    return services.video_service

# ===== HERANÇA DO BASE CONTROLLER =====
class VideoController(BaseController[Video, VideoService]):
    """Controller de vídeos com herança do BaseController"""
    
    def __init__(self):
        super().__init__(router, get_video_service(), "Vídeo")
        self._register_specific_routes()
    
    def _register_specific_routes(self):
        """Registra rotas específicas do domínio de vídeos"""
        
        @self.router.post("", response_model=VideoResponse)
        def create_video(
            video_data: VideoCreateRequest,
            video_service: VideoService = Depends(get_video_service)
        ):
            """Cria um novo vídeo"""
            return video_service.create_video(video_data.title, video_data.source_url)
        
        @self.router.patch("/{video_id}/mark-processing", response_model=VideoResponse)
        def mark_processing(
            video_id: str,
            video_service: VideoService = Depends(get_video_service)
        ):
            """Marca vídeo como processando"""
            video = video_service.mark_processing(video_id)
            if not video:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vídeo não encontrado"
                )
            return video

        @self.router.patch("/{video_id}/mark-ready", response_model=VideoResponse)
        def mark_ready(
            video_id: str,
            video_service: VideoService = Depends(get_video_service)
        ):
            """Marca vídeo como pronto"""
            video = video_service.mark_ready(video_id)
            if not video:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vídeo não encontrado"
                )
            return video

        @self.router.patch("/{video_id}/mark-failed", response_model=VideoResponse)
        def mark_failed(
            video_id: str,
            video_service: VideoService = Depends(get_video_service)
        ):
            """Marca vídeo como falhou"""
            video = video_service.mark_failed(video_id)
            if not video:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vídeo não encontrado"
                )
            return video

# Instanciar o controller para registrar as rotas
video_controller = VideoController()