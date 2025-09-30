from dataclasses import dataclass, field
import datetime
from enum import Enum
from typing import List
from sqlalchemy.dialects.postgresql import UUID
from domain.entities.contas.conta import Conta
from domain.entities.videos.video import Video

class StatusDaPostagem(Enum):
    ENVIADA = "Enviada"
    NAOENVIADA = "Não enviada"

@dataclass
class PostagemAgendada:
    id: str
    descricao: str
    data_para_envio: datetime
    id_video: str
    video: Video
    contas: List[Conta] = field(default_factory=list)
    status: StatusDaPostagem = StatusDaPostagem.NAOENVIADA