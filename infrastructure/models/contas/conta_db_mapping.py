from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, String
from infrastructure.database import Base
from domain.entities.contas.conta import Plataforma


class ContaDbMapping(Base):
    __tablename__ = "contas"

    id = Column(String(36), primary_key=True, index=True)
    nome = Column(String, nullable=False)
    plataforma = Column(Enum(Plataforma), default=Plataforma.TIKTOK)
    datadecadastro = Column(DateTime, default=datetime.now)
