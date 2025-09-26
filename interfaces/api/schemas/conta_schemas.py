from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from domain.entities.contas.conta import Plataforma

class ContaCreateRequest(BaseModel):
    """Schema para criação de conta"""
    id: str
    nome: str
    plataforma: Plataforma
    dataDeCadastro: datetime

class ContaUpdateRequest(BaseModel):
    """Schema para atualização de conta"""
    id: str
    nome: str
    plataforma: Plataforma
    dataDeCadastro: datetime

class ContaResponse(BaseModel):
    """Schema para resposta de conta"""
    id: str
    nome: str
    plataforma: Plataforma
    dataDeCadastro: datetime

model_config = {
        "from_attributes": True  # Pydantic v2
    }