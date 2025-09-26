from dataclasses import dataclass
import datetime
from enum import Enum
import uuid


class Plataforma(Enum):
    YOUTUBE_SHORTS = "Youtube Shorts"
    TIKTOK = "TikTok"

@dataclass
class Conta:
    id: str
    nome: str
    datadecadastro: datetime
    plataforma: Plataforma = Plataforma.TIKTOK

    @staticmethod
    def create_new(nome: str, plataforma: Plataforma) -> "Conta":
        return Conta(
            id=str(uuid.uuid4()),      
            nome=nome,
            datadecadastro=datetime.datetime.now(),
            plataforma=plataforma     
        )
    