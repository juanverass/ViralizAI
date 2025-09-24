from fastapi import APIRouter, Depends, Request, HTTPException, status
from typing import List
from app.services.service_registration_block import ServiceRegistrationBlock
from app.services.videos.video_service import VideoService
from interfaces.api.schemas.video_schemas import VideoCreateRequest, VideoUpdateRequest, VideoResponse
from domain.entities.videos.video import Video

router = APIRouter()

def get_services(request: Request) -> ServiceRegistrationBlock:
    return request.app.state.services

def get_video_service(services: ServiceRegistrationBlock = Depends(get_services)) -> VideoService:
    return services.video_service

@router.post("", response_model=VideoResponse)
def create_video(
    video_data: VideoCreateRequest,
    video_service: VideoService = Depends(get_video_service)
):
    """Cria um novo vídeo"""
    return video_service.create_video(video_data.title, video_data.source_url)

@router.get("", response_model=List[VideoResponse])
def get_all_videos(video_service: VideoService = Depends(get_video_service)):
    """Lista todos os vídeos"""
    return video_service.get_all()

@router.get("/{video_id}", response_model=VideoResponse)
def get_video_by_id(
    video_id: str,
    video_service: VideoService = Depends(get_video_service)
):
    """Busca vídeo por ID"""
    video = video_service.get_by_id(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vídeo não encontrado"
        )
    return video

@router.put("/{video_id}", response_model=VideoResponse)
def update_video(
    video_id: str,
    video_data: VideoUpdateRequest,
    video_service: VideoService = Depends(get_video_service)
):
    """Atualiza um vídeo"""
    video = video_service.get_by_id(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vídeo não encontrado"
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = video_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(video, key):
            setattr(video, key, value)
    
    return video_service.update(video)

@router.delete("/{video_id}")
def delete_video(
    video_id: str,
    video_service: VideoService = Depends(get_video_service)
):
    """Remove um vídeo"""
    video = video_service.get_by_id(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vídeo não encontrado"
        )
    
    video_service.delete_by_id(video_id)
    return {"message": "Vídeo removido com sucesso"}

# Rotas específicas do domínio
@router.patch("/{video_id}/mark-processing", response_model=VideoResponse)
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

@router.patch("/{video_id}/mark-ready", response_model=VideoResponse)
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

@router.patch("/{video_id}/mark-failed", response_model=VideoResponse)
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