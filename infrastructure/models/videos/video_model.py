from sqlalchemy import Column, String, Enum, Float
from infrastructure.database import Base
import enum

class StatusDoVideo(Enum):
    PENDENTE = "Pendente"
    PROCESSING = "Processando"
    READY = "pronto"
    FAILED = "Falhou"

class VideoModel(Base):
    __tablename__ = "videos"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    local_path = Column(String, nullable=True)
    status = Column(Enum(StatusDoVideo), default=StatusDoVideo.PENDING)
    duration = Column(Float, nullable=True)
    language = Column(String, default="pt-BR")
