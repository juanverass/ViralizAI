from typing import Optional
from pydantic import BaseModel
from domain.entities.videos.video import StatusDoVideo

class GenerateVideoRequest(BaseModel):
    roteiro: str

class VideoCreateRequest(BaseModel):
    """Schema para criação de vídeo"""
    title: str
    source_url: str

class VideoUpdateRequest(BaseModel):
    """Schema para atualização de vídeo"""
    title: Optional[str] = None
    source_url: Optional[str] = None
    local_path: Optional[str] = None
    status: Optional[StatusDoVideo] = None
    duration: Optional[float] = None
    language: Optional[str] = None

class VideoResponse(BaseModel):
    """Schema para resposta de vídeo"""
    id: str
    title: str
    source_url: str
    local_path: Optional[str] = None
    status: StatusDoVideo
    duration: Optional[float] = None
    language: str

model_config = {
        "from_attributes": True  # Pydantic v2
    }
