import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String,Enum
from domain.entities.postagens_agendadas.postagem_agendada import StatusDaPostagem
from infrastructure.database import Base
from sqlalchemy.orm import relationship

class PostagemAgendadaDbMapping(Base):
    __tablename__ = "postagemagendada"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    descricao = Column(String, nullable=False)
    data_para_envio = Column(DateTime, nullable=True)
    status = Column(Enum(StatusDaPostagem), default=StatusDaPostagem.NAOENVIADA)
    id_video = Column(String(36), ForeignKey("videos.id"), nullable=False)
    video = relationship("VideoDbMapping")
    
    contas = relationship(
        "ContaDbMapping",
        secondary="postagemagendadanaconta",
        viewonly=True
    )