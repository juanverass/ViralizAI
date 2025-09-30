from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.database import Base

postagem_da_conta = Table(
    "postagemagendadanaconta",
    Base.metadata,
    Column("idPostagem", UUID(as_uuid=True), ForeignKey("postagemagendada.id"), primary_key=True),
    Column("idConta", UUID(as_uuid=True), ForeignKey("contas.id"), primary_key=True)
)