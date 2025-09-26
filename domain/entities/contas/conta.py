from dataclasses import dataclass
import datetime
from enum import Enum


class Plataforma(Enum):
    Tiktok = "TikTok"
    YoutubeShorts = "Youtube Shorts"

@dataclass
class Conta:
    Id: str
    Nome: str
    Plataforma: Plataforma
    DataDeCadastro: datetime
    