from sqlalchemy import Column, String, Enum, Float
from infrastructure.database import Base
from domain.entities.videos.video import StatusDoVideo

class VideoModel(Base):
    __tablename__ = "videos"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    local_path = Column(String, nullable=True)
    status = Column(Enum(StatusDoVideo), default=StatusDoVideo.PENDENTE)
    duration = Column(Float, nullable=True)
    language = Column(String, default="pt-BR")
