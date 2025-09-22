from dataclasses import dataclass
from enum import Enum
from typing import Optional
import uuid

class StatusDoVideo(Enum):
    PENDENTE = "Pendente"
    PROCESSING = "Processando"
    READY = "pronto"
    FAILED = "Falhou"

@dataclass
class Video:
    id: str
    title: str
    source_url: str
    local_path: Optional[str] = None
    status: StatusDoVideo = StatusDoVideo.PENDENTE
    duration: Optional[float] = None
    language: str = "pt"

    @staticmethod
    def create_new(title: str, source_url: str) -> "Video":
        return Video(
            id=str(uuid.uuid4()),  # gera UUID automaticamente
            title=title,
            source_url=source_url
        )