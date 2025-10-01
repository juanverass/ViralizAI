
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostagemAgendadaCreateRequest(BaseModel):
    """Schema para criação de vídeo"""
    descricao: str
    data_para_envio: datetime
    id_video: str

class PostagemAgendadaUpdateRequest(BaseModel):
    """Schema para atualização de vídeo"""
    descricao: str
    data_para_envio: Optional[datetime] = None
    id_video: str

class PostagemAgendadaResponse(BaseModel):
    """Schema para resposta de vídeo"""
    id: str
    descricao: str
    data_para_envio: datetime

model_config = {
        "from_attributes": True  # Pydantic v2
    }