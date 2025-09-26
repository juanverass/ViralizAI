from enum import Enum
from sqlalchemy import Column, DateTime, String
from infrastructure.database import Base
from domain.entities.contas.conta import Plataforma


class ContaDbMapping(Base):
    __tablename__ = "contas"

    Id = Column(String(36), primary_key=True, index=True)
    Nome = Column(String, nullable=False)
    Plataforma = Column(Enum(Plataforma), default=None)
    DataDeCadastro = Column(DateTime, nullable=False)
