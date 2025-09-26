## 🏗 Arquitetura Hexagonal

```text
   ┌─────────────────────────────┐
   │        Interfaces           │
   │  (API REST / CLI / n8n)    │
   └─────────────┬──────────────┘
                 │
                 ▼
   ┌─────────────────────────────┐
   │       Application           │
   │ (Use Cases / App Services)  │
   └─────────────┬──────────────┘
                 │
        ┌────────┴────────┐
        │                 │
  ┌───────────────┐  ┌───────────────┐
  │     Domain    │  │ Infrastructure │
  │ (Entities +   │  │ (APIs externas,│
  │ Domain Services) │ banco, storage) │
  └───────────────┘  └───────────────┘
```

💡 **Legenda do fluxo**:

1. O usuário faz uma requisição (Interface).
2. A **Application** orquestra os casos de uso, validando regras do domínio.
3. Os **Domain Services** aplicam regras de negócio puras.
4. A **Infrastructure** executa tarefas externas (API de vídeo, dublagem, armazenamento).
5. Resultado sobe novamente até a Interface para o usuário.

---

## 🚀 Estrutura de Pastas

```
ViralizAI/
├── app/
│   ├── main.py
│   └── services/
│       ├── service_registration_block.py
│       └── videos/
│           └── video_service.py
├── domain/
│   └── entities/
│       └── videos/
│           └── video.py
├── infrastructure/
│   ├── models/videos/video_model.py
│   ├── mappers/videos/video_mapper.py
│   └── repositories/
│       ├── comuns/base_repository.py
│       └── videos/video_repository.py
└── interfaces/api/
    ├── video_controller.py
    └── router_registration_block.py
```

---

## 📌 Tutorial Passo a Passo: Criando uma Nova Entidade

Este tutorial foi feito para que os novos **desenvolvedores se baseiem** ao entrar no projeto. Aqui explicamos **cada camada, cada decisão e cada passo** para criar uma entidade e conectá-la à API.

### 1️⃣ Criar a Entidade de Domínio

> **Objetivo**: Representar o conceito de negócio.

Arquivo: `domain/entities/videos/video.py`

```python
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
```

**O que você está fazendo:**

- Define os dados essenciais do vídeo.
- Define o status atual do vídeo.
- Mantém o domínio **puro**, sem dependência de banco ou frameworks.

### 2️⃣ Criar o Modelo ORM

> **Objetivo**: Representar a entidade no banco de dados.

Arquivo: `infrastructure/models/videos/video_db_mapping.py`

```python
from sqlalchemy import Column, String, Enum, Float
from infrastructure.database import Base
from domain.entities.videos.video import StatusDoVideo


class VideoDbMapping(Base):
    __tablename__ = "videos"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    local_path = Column(String, nullable=True)
    status = Column(Enum(StatusDoVideo), default=StatusDoVideo.PENDENTE)
    duration = Column(Float, nullable=True)
    language = Column(String, default="pt-BR")
```

**O que você está fazendo:**

- Define como o vídeo será salvo no banco.
- Isola as regras de persistência, mantendo a entidade independente.

### 3️⃣ Criar o Mapper

> **Objetivo**: Converter entre entidade de domínio e modelo ORM.

Arquivo: `infrastructure/mappers/videos/video_persistence_mapper.py`

```python
from domain.entities.videos.video import StatusDoVideo, Video
from infrastructure.models.videos.video_db_mapping import VideoDbMapping

class VideoPersistenceMapper:
    """Mapper entre Video (domínio) e VideoDbMapping (ORM)"""
    
    @staticmethod
    def to_model(entity: Video) -> VideoDbMapping:
        return VideoDbMapping(
            id=entity.id,
            title=entity.title,
            source_url=entity.source_url,
            local_path=entity.local_path,
            status=entity.status.value,
            duration=entity.duration,
            language=entity.language
        )

    @staticmethod
    def to_entity(model: VideoDbMapping) -> Video:
        return Video(
            id=model.id,
            title=model.title,
            source_url=model.source_url,
            local_path=model.local_path,
            status=model.status,
            duration=model.duration,
            language=model.language
        )
```

**O que você está fazendo:**

- Cria a ponte entre domínio e banco.
- Permite trocar ORM ou banco sem afetar o domínio.

### 4️⃣ Criar o Repository Port (Contrato)

> **Objetivo**: Definir quais operações o repositório deve oferecer.

Arquivo: `domain/repositories/video_repository_port.py`

```python
from typing import Protocol, Optional, List
from domain.entities.videos.video import Video
from domain.repositories.base_repository_port import BaseRepositoryPort

class VideoRepositoryPort(BaseRepositoryPort[Video]):
    """Contrato para repositório de vídeos"""
```

**O que você está fazendo:**

- Define o contrato, sem implementação.
- Permite mudar a implementação sem quebrar o domínio.

### 5️⃣ Criar o Repository (Implementação)

> **Objetivo**: Implementar o contrato usando SQLAlchemy.

Arquivo: `infrastructure/repositories/videos/video_repository.py`

```python
from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities.videos.video import Video, StatusDoVideo
from domain.repositories.video_repository_port import VideoRepositoryPort
from infrastructure.mappers.videos.video_persistence_mapper import VideoPersistenceMapper
from infrastructure.models.videos.video_db_mapping import VideoDbMapping
from infrastructure.repositories.comuns.base_repository import BaseRepository

class VideoRepository(BaseRepository[Video, VideoDbMapping], VideoRepositoryPort):
    """Implementação do repositório de vídeos usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        super().__init__(session, VideoDbMapping, VideoPersistenceMapper)
```

**O que você está fazendo:**

- Herda CRUD genérico do BaseRepository.
- Conecta Mapper e ORM.
- Não coloca regras de negócio aqui (isso é responsabilidade do Service).

### 6️⃣ Criar o App Service

> **Objetivo**: Orquestrar regras de negócio e casos de uso.

Arquivo: `app/services/videos/video_service.py`

```python
from typing import Optional
from domain.entities.videos.video import Video, StatusDoVideo
from domain.repositories.video_repository_port import VideoRepositoryPort as _repository
from app.services.base_app_service import BaseAppService

class VideoService(BaseAppService[Video]):
    """Serviço de vídeos - casos de uso específicos do domínio"""
    
    def __init__(self, repository: _repository):
        super().__init__(repository)

    def create_video(self, title: str, source_url: str) -> Video:
        """Cria um novo vídeo"""
        video = Video.create_new(title, source_url)
        return  _repository.add(video)
     

```

**O que você está fazendo:**

- Recebe repositório via dependência.
- Usa CRUD genérico e adiciona casos de uso específicos.
- Mantém separação de responsabilidades.

### 7️⃣ Criar os Schemas Pydantic

Arquivo: `interfaces/api/schemas/video_schemas.py`

```python
from typing import Optional
from pydantic import BaseModel
from domain.entities.videos.video import StatusDoVideo

class VideoCreateRequest(BaseModel):
    """Schema para criação de vídeo"""
    title: str
    source_url: str

class VideoUpdateRequest(BaseModel):
    """Schema para atualização de vídeo"""
    title: Optional[str] = None
    source_url: Optional[str] = None
    local_path: Optional[str] = None
    status: Optional[StatusDoVideo] = None
    duration: Optional[float] = None
    language: Optional[str] = None

class VideoResponse(BaseModel):
    """Schema para resposta de vídeo"""
    id: str
    title: str
    source_url: str
    local_path: Optional[str] = None
    status: StatusDoVideo
    duration: Optional[float] = None
    language: str

model_config = {
        "from_attributes": True  # Pydantic v2
    }

```

**O que você está fazendo:**

- Define dados válidos de entrada e saída.
- Garante documentação automática (Swagger).

### 8️⃣ Criar o Controller

Arquivo: `interfaces/api/video_controller.py`

```python
from fastapi import APIRouter, HTTPException, status
from infrastructure.database import SessionLocal
from infrastructure.repositories.videos.video_repository import VideoRepository
from interfaces.api.base_controller import BaseController
from app.services.videos.video_service import VideoService
from interfaces.api.schemas.video_schemas import VideoCreateRequest, VideoUpdateRequest, VideoResponse

router = APIRouter()

# Aqui usamos BaseController passando:
# EntityType = ORM entity do vídeo (geralmente Video)
# CreateUpdateModelType = VideoUpdateRequest (ou VideoCreateRequest, depende do método)
# ResponseModelType = VideoResponse
# ServiceType = VideoService
session = SessionLocal()

video_repository = VideoRepository(session) 
video_service = VideoService(video_repository)
video_controller = BaseController(
    router=router,
    service= video_service,
    response_model=VideoResponse,
    entity_name="Vídeo"
)

```

**Caso seja necessário criar mais endpoints que não sejam padrão, segue o exemplo abaixo:**

```python
from fastapi import APIRouter, HTTPException, status
from infrastructure.database import SessionLocal
from infrastructure.repositories.videos.video_repository import VideoRepository
from interfaces.api.base_controller import BaseController
from app.services.videos.video_service import VideoService
from interfaces.api.schemas.video_schemas import VideoCreateRequest, VideoUpdateRequest, VideoResponse

router = APIRouter()

# Aqui usamos BaseController passando:
# EntityType = ORM entity do vídeo (geralmente Video)
# CreateUpdateModelType = VideoUpdateRequest (ou VideoCreateRequest, depende do método)
# ResponseModelType = VideoResponse
# ServiceType = VideoService
session = SessionLocal()

video_repository = VideoRepository(session) 
video_service = VideoService(video_repository)
video_controller = BaseController(
    router=router,
    service= video_service,
    response_model=VideoResponse,
    entity_name="Vídeo"
)

@router.patch("/videos/{video_id}/mark-processing", response_model=VideoResponse)
def mark_processing(video_id: str):
    """
    Marca um vídeo específico como 'Processing'.
    """
    video = video_service.mark_processing(video_id)
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vídeo não encontrado"
        )
    
    return video
```
- Endpoints automáticos: `GET /videos`, `GET /videos/{id}`, `PUT /videos/{id}`, `DELETE /videos/{id}`
- Endpoints específicos: `POST /videos`, `PATCH /videos/{id}/mark-processing` etc.

### 9️⃣ Registrar nos Blocks

- **RepositoryRegistrationBlock**: instancia repositórios.
- **ServiceRegistrationBlock**: instancia services usando repositórios.
- **RouterRegistrationBlock**: registra routers na aplicação FastAPI.

### 10️⃣ Resultado Final

Após seguir o passo a passo:

- Entidade: `Video`
- Mapper: `VideoPersistenceMapper`
- Repository: `VideoRepository`
- Service: `VideoService`
- Controller: `VideoController`
- Schemas: `VideoCreateRequest`, `VideoUpdateRequest`, `VideoResponse`

**Endpoints disponíveis:**

- `POST /videos`
- `GET /videos`
- `GET /videos/{id}`
- `PUT /videos/{id}`
- `DELETE /videos/{id}`

---