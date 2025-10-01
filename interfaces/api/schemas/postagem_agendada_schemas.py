from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from domain.entities.postagens_agendadas.postagem_agendada import StatusDaPostagem
from domain.entities.videos.video import Video
from domain.entities.contas.conta import Conta


class PostagemAgendadaCreateRequest(BaseModel):
    """Schema para criação de postagem agendada"""
    descricao: str
    data_para_envio: datetime
    id_video: str
    contas: Optional[List[Conta]] = []


class PostagemAgendadaUpdateRequest(BaseModel):
    """Schema para atualização de postagem agendada"""
    descricao: Optional[str] = None
    data_para_envio: Optional[datetime] = None
    id_video: Optional[str] = None
    contas: Optional[List[Conta]] = None
    status: Optional[StatusDaPostagem] = None


class PostagemAgendadaResponse(BaseModel):
    """Schema para resposta de postagem agendada"""
    id: str
    descricao: str
    data_para_envio: datetime
    id_video: str
    video: Video
    contas: List[Conta]
    status: StatusDaPostagem

    model_config = {
        "from_attributes": True  # Pydantic v2
    }
