# ViralizAI 🚀

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)  
[![Build](https://img.shields.io/badge/Build-Pending-orange)](https://github.com/seu-usuario/viralizai/actions)  
[![Coverage](https://img.shields.io/badge/Coverage-0%25-red)](https://github.com/seu-usuario/viralizai/actions)  

**ViralizAI** é uma plataforma em Python para **criação automatizada de vídeos curtos (TikTok / YouTube Shorts)** usando IA. O sistema gera vídeos, dublagens e legendas automaticamente, podendo processar conteúdos via links ou prompts de texto.

---

## 🌟 Funcionalidades

- Criação de vídeos a partir de **prompts ou links de vídeos**.  
- **Dublagem automática** (via ElevenLabs API).  
- **Geração automática de legendas**.  
- Integração com **n8n** para workflows automatizados.  
- Arquitetura **hexagonal**, modular e testável.  

---

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

## 🛠 Tecnologias

- Python 3.11+  
- FastAPI  
- SQLAlchemy  
- Requests / HTTPX  
- ElevenLabs API  
- n8n  
- pytest  

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

## 📌 Tutorial: Criando uma Nova Entidade

Este tutorial mostra como criar uma nova entidade seguindo a arquitetura hexagonal do ViralizAI. Usaremos **Usuario** como exemplo.

> **💡 O que é Arquitetura Hexagonal?**
> 
> A arquitetura hexagonal (também conhecida como Ports and Adapters) separa o código em camadas bem definidas:
> - **Domain**: Regras de negócio puras (entidades, enums, contratos)
> - **Application**: Casos de uso e orquestração (services)
> - **Infrastructure**: Implementações técnicas (banco, APIs externas)
> - **Interfaces**: Pontos de entrada (API REST, CLI, etc.)

### 1️⃣ **Criar a Entidade de Domínio**

> **🎯 Objetivo**: Criar a entidade que representa o conceito de negócio no domínio.

A entidade de domínio é o coração da aplicação. Ela contém:
- **Dados**: Propriedades da entidade
- **Regras**: Validações e comportamentos
- **Enums**: Estados possíveis
- **Factory Methods**: Métodos para criar instâncias

Crie o arquivo `domain/entities/usuarios/usuario.py`:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import uuid

class StatusUsuario(Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"
    BLOQUEADO = "Bloqueado"

@dataclass
class Usuario:
    id: str
    nome: str
    email: str
    telefone: Optional[str] = None
    status: StatusUsuario = StatusUsuario.ATIVO
    data_criacao: Optional[str] = None

    @staticmethod
    def create_new(nome: str, email: str) -> "Usuario":
        return Usuario(
            id=str(uuid.uuid4()),
            nome=nome,
            email=email
        )
```

### 2️⃣ **Criar o Mapeamento de Banco**

> **🎯 Objetivo**: Criar a representação da entidade no banco de dados.

O mapeamento de banco é responsável por:
- **Estrutura**: Definir como a entidade é armazenada no banco
- **Tipos**: Mapear tipos Python para tipos SQL
- **Constraints**: Definir regras de integridade (unique, nullable, etc.)
- **Relacionamentos**: Chaves estrangeiras e associações

> **⚠️ Importante**: Esta camada está na **Infrastructure** porque depende de tecnologia específica (SQLAlchemy).

Crie o arquivo `infrastructure/models/usuarios/usuario_db_mapping.py`:

```python
from sqlalchemy import Column, String, Enum, DateTime
from infrastructure.database import Base
from domain.entities.usuarios.usuario import StatusUsuario

class UsuarioDbMapping(Base):
    __tablename__ = "usuarios"

    id = Column(String(36), primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=True)
    status = Column(Enum(StatusUsuario), default=StatusUsuario.ATIVO)
    data_criacao = Column(DateTime, nullable=True)
```

### 3️⃣ **Criar o Mapper**

> **🎯 Objetivo**: Criar a ponte entre a entidade de domínio e o mapeamento de banco.

O mapper é responsável por:
- **Conversão**: Transformar entidade ↔ model de banco
- **Isolamento**: Manter domínio independente da tecnologia de persistência
- **Mapeamento**: Garantir que todos os campos sejam convertidos corretamente
- **Bidirecional**: Funciona nos dois sentidos (to_model e to_entity)

> **💡 Por que precisamos do Mapper?**
> 
> O domínio não deve conhecer detalhes de implementação. O mapper permite que:
> - A entidade permaneça "pura" (sem dependências de SQLAlchemy)
> - Possamos trocar de ORM sem afetar o domínio
> - O código seja mais testável e flexível

Crie o arquivo `infrastructure/mappers/usuarios/usuario_mapper.py`:

```python
from domain.entities.usuarios.usuario import StatusUsuario, Usuario
from infrastructure.models.usuarios.usuario_db_mapping import UsuarioDbMapping

class UsuarioMapper:
    @staticmethod
    def to_model(entity: Usuario) -> UsuarioDbMapping:
        return UsuarioDbMapping(
            id=entity.id,
            nome=entity.nome,
            email=entity.email,
            telefone=entity.telefone,
            status=entity.status,
            data_criacao=entity.data_criacao
        )

    @staticmethod
    def to_entity(model: UsuarioDbMapping) -> Usuario:
        return Usuario(
            id=model.id,
            nome=model.nome,
            email=model.email,
            telefone=model.telefone,
            status=StatusUsuario(model.status.value),
            data_criacao=model.data_criacao
        )
```

### 4️⃣ **Criar o Repository Port (Contrato)**

> **🎯 Objetivo**: Definir o contrato que o repositório deve implementar.

O Repository Port é um **contrato** que define:
- **Interface**: Quais operações o repositório deve oferecer
- **Assinaturas**: Tipos de entrada e saída de cada método
- **Independência**: O domínio não conhece a implementação

> **💡 O que é um Port?**
> 
> Um "Port" é como uma interface em C# - define **o que** fazer, não **como** fazer.
> - O domínio define os contratos (Ports)
> - A infraestrutura implementa os contratos (Adapters)
> - Isso permite trocar implementações sem afetar o domínio

> **🔧 Protocol vs Interface**: Em Python, usamos `Protocol` que funciona como interface, mas com duck typing.

Crie o arquivo `domain/repositories/usuario_repository_port.py`:

```python
from typing import Protocol, Optional, List
from domain.entities.usuarios.usuario import Usuario

class UsuarioRepositoryPort(Protocol):
    """Contrato para repositório de usuários"""
    
    def add(self, entity: Usuario) -> Usuario: ...
    def get_all(self) -> List[Usuario]: ...
    def get_by_id(self, id_entity: str) -> Optional[Usuario]: ...
    def update(self, entity: Usuario) -> Usuario: ...
    def delete(self, entity: Usuario) -> None: ...
    def delete_by_id(self, id_entity: str) -> None: ...
```

### 5️⃣ **Criar o Repository (Implementação)**

> **🎯 Objetivo**: Implementar o contrato do repositório usando SQLAlchemy.

O Repository é a **implementação concreta** que:
- **Herda**: Do `BaseRepository` genérico (CRUD automático)
- **Implementa**: O Protocol definido no domínio
- **Usa**: SQLAlchemy para persistência
- **Mapeia**: Entre entidade e model via mapper

> **🏗️ Arquitetura do Repository:**
> 
> ```
> UsuarioRepository
> ├── BaseRepository[Usuario, UsuarioDbMapping]  # CRUD genérico
> └── UsuarioRepositoryPort                       # Contrato do domínio
> ```
> 
> **Benefícios:**
> - **CRUD automático**: Herda operações básicas do BaseRepository
> - **Type Safety**: Type hints garantem tipos corretos
> - **Flexibilidade**: Pode adicionar métodos específicos
> - **Testabilidade**: Fácil de mockar para testes

Crie o arquivo `infrastructure/repositories/usuarios/usuario_repository.py`:

```python
from typing import Optional
from sqlalchemy.orm import Session
from domain.entities.usuarios.usuario import Usuario, StatusUsuario
from domain.repositories.usuario_repository_port import UsuarioRepositoryPort
from infrastructure.mappers.usuarios.usuario_mapper import UsuarioMapper
from infrastructure.models.usuarios.usuario_db_mapping import UsuarioDbMapping
from infrastructure.repositories.comuns.base_repository import BaseRepository

class UsuarioRepository(BaseRepository[Usuario, UsuarioDbMapping], UsuarioRepositoryPort):
    """Implementação do repositório de usuários usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        super().__init__(session, UsuarioDbMapping, UsuarioMapper)
    
    def update_status(self, usuario_id: str, status: StatusUsuario) -> Optional[Usuario]:
        """Atualiza status de um usuário específico"""
        usuario = self.get_by_id(usuario_id)
        if usuario:
            usuario.status = status
            return self.update(usuario)
        return None
```

### 6️⃣ **Criar o App Service**

> **🎯 Objetivo**: Criar a camada de casos de uso que orquestra as operações de negócio.

O App Service é responsável por:
- **Casos de Uso**: Implementar regras de negócio específicas
- **Orquestração**: Coordenar entre repositório e domínio
- **Validação**: Aplicar regras de negócio antes de persistir
- **Transações**: Garantir consistência das operações

> **🏗️ Arquitetura do Service:**
> 
> ```
> UsuarioService
> ├── BaseAppService[Usuario]           # CRUD padrão herdado
> └── Métodos específicos do domínio    # Regras de negócio
> ```
> 
> **Benefícios:**
> - **Herança**: Acesso automático a operações CRUD básicas
> - **Especialização**: Métodos específicos para o domínio
> - **Injeção**: Recebe repositório via Protocol (testável)
> - **Separação**: Casos de uso isolados da infraestrutura

> **💡 Por que herdar de BaseAppService?**
> 
> Evita duplicação de código. O service herda automaticamente:
> - `add()`, `get_all()`, `get_by_id()`, `update()`, `delete()`
> - E pode focar apenas nas regras específicas do domínio

Crie o arquivo `app/services/usuarios/usuario_service.py`:

```python
from typing import Optional
from domain.entities.usuarios.usuario import Usuario, StatusUsuario
from domain.repositories.usuario_repository_port import UsuarioRepositoryPort
from app.services.base_app_service import BaseAppService

class UsuarioService(BaseAppService[Usuario]):
    """Serviço de usuários - casos de uso específicos do domínio"""
    
    def __init__(self, repository: UsuarioRepositoryPort):
        super().__init__(repository)

    def create_usuario(self, nome: str, email: str) -> Usuario:
        """Cria um novo usuário"""
        usuario = Usuario.create_new(nome, email)
        return self.add(usuario)

    def block_usuario(self, usuario_id: str) -> Optional[Usuario]:
        """Bloqueia um usuário"""
        return self._repository.update_status(usuario_id, StatusUsuario.BLOQUEADO)

    def activate_usuario(self, usuario_id: str) -> Optional[Usuario]:
        """Ativa um usuário"""
        return self._repository.update_status(usuario_id, StatusUsuario.ATIVO)
```

### 7️⃣ **Criar os Schemas Pydantic**

> **🎯 Objetivo**: Definir a estrutura de dados para entrada e saída da API.

Os Schemas Pydantic são responsáveis por:
- **Validação**: Garantir que os dados recebidos estão corretos
- **Serialização**: Converter entre JSON e objetos Python
- **Documentação**: Gerar automaticamente a documentação da API
- **Type Safety**: Garantir tipos corretos em tempo de execução

> **📋 Tipos de Schema:**
> 
> - **CreateRequest**: Dados necessários para criar uma entidade
> - **UpdateRequest**: Dados opcionais para atualizar (todos os campos opcionais)
> - **Response**: Estrutura de resposta da API (pode incluir campos calculados)

> **💡 Por que separar em schemas diferentes?**
> 
> - **Segurança**: Evita exposição de campos internos
> - **Flexibilidade**: Diferentes endpoints podem ter diferentes estruturas
> - **Validação**: Regras específicas para cada operação
> - **Evolução**: Mudanças em um schema não afetam outros

Crie o arquivo `interfaces/api/schemas/usuario_schemas.py`:

```python
from typing import Optional
from pydantic import BaseModel
from domain.entities.usuarios.usuario import StatusUsuario

class UsuarioCreateRequest(BaseModel):
    """Schema para criação de usuário"""
    nome: str
    email: str
    telefone: Optional[str] = None

class UsuarioUpdateRequest(BaseModel):
    """Schema para atualização de usuário"""
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    status: Optional[StatusUsuario] = None

class UsuarioResponse(BaseModel):
    """Schema para resposta de usuário"""
    id: str
    nome: str
    email: str
    telefone: Optional[str] = None
    status: StatusUsuario
    data_criacao: Optional[str] = None

    class Config:
        from_attributes = True
```

### 8️⃣ **Criar o Controller**

> **🎯 Objetivo**: Criar os endpoints REST que expõem a funcionalidade via HTTP.

O Controller é responsável por:
- **Endpoints**: Definir rotas HTTP (GET, POST, PUT, DELETE, PATCH)
- **Validação**: Usar schemas Pydantic para validar entrada
- **Tratamento**: Converter erros de domínio em respostas HTTP
- **Documentação**: Gerar documentação automática (Swagger)

> **🏗️ Estrutura do Controller:**
> 
> ```
> UsuarioController
> ├── Endpoints CRUD padrão        # GET, POST, PUT, DELETE
> ├── Endpoints específicos        # PATCH para ações do domínio
> ├── Validação de entrada         # Schemas Pydantic
> ├── Tratamento de erros         # HTTPException
> └── Injeção de dependência      # Service via FastAPI Depends
> ```

> **💡 Padrões de Endpoint:**
> 
> - **POST /usuarios**: Criar novo usuário
> - **GET /usuarios**: Listar todos os usuários
> - **GET /usuarios/{id}**: Buscar usuário específico
> - **PUT /usuarios/{id}**: Atualizar usuário completo
> - **DELETE /usuarios/{id}**: Remover usuário
> - **PATCH /usuarios/{id}/block**: Ação específica do domínio

> **🔧 Injeção de Dependência:**
> 
> O FastAPI usa `Depends()` para injetar o service automaticamente:
> - **Testabilidade**: Fácil de mockar em testes
> - **Reutilização**: Mesmo service usado em múltiplos endpoints
> - **Configuração**: Centralizada no `main.py`

Crie o arquivo `interfaces/api/usuario_controller.py`:

```python
from fastapi import APIRouter, Depends, Request, HTTPException, status
from typing import List
from app.services.service_registration_block import ServiceRegistrationBlock
from app.services.usuarios.usuario_service import UsuarioService
from interfaces.api.schemas.usuario_schemas import UsuarioCreateRequest, UsuarioUpdateRequest, UsuarioResponse
from domain.entities.usuarios.usuario import Usuario

router = APIRouter()

def get_services(request: Request) -> ServiceRegistrationBlock:
    return request.app.state.services

def get_usuario_service(services: ServiceRegistrationBlock = Depends(get_services)) -> UsuarioService:
    return services.usuario_service

@router.post("", response_model=UsuarioResponse)
def create_usuario(
    usuario_data: UsuarioCreateRequest,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """Cria um novo usuário"""
    return usuario_service.create_usuario(usuario_data.nome, usuario_data.email)

@router.get("", response_model=List[UsuarioResponse])
def get_all_usuarios(usuario_service: UsuarioService = Depends(get_usuario_service)):
    """Lista todos os usuários"""
    return usuario_service.get_all()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario_by_id(
    usuario_id: str,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """Busca usuário por ID"""
    usuario = usuario_service.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario

# Rotas específicas do domínio
@router.patch("/{usuario_id}/block", response_model=UsuarioResponse)
def block_usuario(
    usuario_id: str,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """Bloqueia um usuário"""
    usuario = usuario_service.block_usuario(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario

@router.patch("/{usuario_id}/activate", response_model=UsuarioResponse)
def activate_usuario(
    usuario_id: str,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    """Ativa um usuário"""
    usuario = usuario_service.activate_usuario(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario
```

### 9️⃣ **Registrar nos Blocks**

> **🎯 Objetivo**: Conectar todas as peças da arquitetura através da injeção de dependência.

Os Registration Blocks são responsáveis por:
- **Configuração**: Centralizar a criação de todas as dependências
- **Injeção**: Conectar repositórios → services → controllers
- **Singleton**: Garantir que as mesmas instâncias sejam reutilizadas
- **Ordem**: Definir a sequência correta de criação

> **🏗️ Fluxo de Injeção:**
> 
> ```
> main.py
> ├── SessionLocal()                    # Conexão com banco
> ├── RepositoryRegistrationBlock       # Cria repositórios
> ├── ServiceRegistrationBlock          # Cria services (recebe repositórios)
> └── RouterRegistrationBlock          # Registra rotas
> ```

> **💡 Por que usar Registration Blocks?**
> 
> - **Organização**: Cada camada tem seu próprio bloco
> - **Manutenção**: Fácil adicionar/remover dependências
> - **Testabilidade**: Fácil de mockar para testes
> - **Flexibilidade**: Pode trocar implementações facilmente

**RepositoryRegistrationBlock** (`infrastructure/repositories/repository_registration_block.py`):
```python
from infrastructure.repositories.videos.video_repository import VideoRepository
from infrastructure.repositories.usuarios.usuario_repository import UsuarioRepository

class RepositoryRegistrationBlock:
    def __init__(self, session):
        self.videos = VideoRepository(session)
        self.usuarios = UsuarioRepository(session)
```

**ServiceRegistrationBlock** (`app/services/service_registration_block.py`):
```python
from app.services.videos.video_service import VideoService
from app.services.usuarios.usuario_service import UsuarioService
from infrastructure.repositories.repository_registration_block import RepositoryRegistrationBlock

class ServiceRegistrationBlock:
    def __init__(self, repositories: RepositoryRegistrationBlock):
        self.video_service = VideoService(repositories.videos)
        self.usuario_service = UsuarioService(repositories.usuarios)
```

**RouterRegistrationBlock** (`interfaces/api/router_registration_block.py`):
```python
from fastapi import FastAPI
from interfaces.api import video_controller, usuario_controller

class RouterRegistrationBlock:
    def __init__(self):
        self.routers = [
            (video_controller.router, "/videos", ["Vídeos"]),
            (usuario_controller.router, "/usuarios", ["Usuários"]),
        ]

    def register_all(self, app: FastAPI):
        for router, prefix, tags in self.routers:
            app.include_router(router, prefix=prefix, tags=tags)
```

### ✅ **Resultado Final**

Após seguir este tutorial, você terá:

- **Entidade**: `Usuario` com regras de domínio
- **Mapeamento**: `UsuarioDbMapping` para persistência
- **Repository**: `UsuarioRepository` com CRUD completo
- **Service**: `UsuarioService` com casos de uso
- **Controller**: Endpoints REST completos
- **Schemas**: Validação de entrada/saída

**Endpoints disponíveis:**
- `POST /usuarios` - Criar usuário
- `GET /usuarios` - Listar todos
- `GET /usuarios/{id}` - Buscar por ID
- `PATCH /usuarios/{id}/block` - Bloquear usuário
- `PATCH /usuarios/{id}/activate` - Ativar usuário

---

## 🎓 **Resumo da Arquitetura Hexagonal**

### **📋 Camadas e Responsabilidades:**

| Camada | Responsabilidade | Exemplo |
|--------|------------------|---------|
| **Domain** | Regras de negócio puras | `Usuario`, `StatusUsuario`, `UsuarioRepositoryPort` |
| **Application** | Casos de uso e orquestração | `UsuarioService` |
| **Infrastructure** | Implementações técnicas | `UsuarioRepository`, `UsuarioDbMapping`, `UsuarioMapper` |
| **Interfaces** | Pontos de entrada | `UsuarioController`, `UsuarioSchemas` |

### **🔄 Fluxo de Dados:**

```
HTTP Request → Controller → Service → Repository → Database
     ↓              ↓         ↓          ↓
HTTP Response ← Controller ← Service ← Repository ← Database
```

### **💡 Benefícios Alcançados:**

- **Testabilidade**: Cada camada pode ser testada independentemente
- **Flexibilidade**: Fácil trocar implementações (ex: SQLAlchemy → MongoDB)
- **Manutenibilidade**: Código organizado e responsabilidades claras
- **Escalabilidade**: Fácil adicionar novas funcionalidades
- **Reutilização**: BaseRepository e BaseAppService para qualquer entidade

### **🚀 Próximos Passos:**

1. **Testes**: Criar testes unitários para cada camada
2. **Validações**: Adicionar validações de negócio mais complexas
3. **Relacionamentos**: Implementar relacionamentos entre entidades
4. **Cache**: Adicionar camada de cache
5. **Logs**: Implementar logging estruturado

---



---

## 📌 Fluxo de criação de vídeo (Mermaid)

```mermaid
flowchart TD
    A[Interface: POST /videos] --> B[Service: VideoService.create_video]
    B --> C[Repository: VideoRepository.add]
    C --> D[Database: VideoModel insert]
    D --> C
    C --> B
    B --> A[Retorna Video criado]
```

---

## 🚀 Como Começar

1. Clone o repositório:  
```bash
git clone <repo-url>
cd ViralizAI
```

2. Instale as dependências:  
```bash
pip install -r requirements.txt
```

3. Rode a aplicação mínima:  
```bash
python -m uvicorn app.main:app --reload
```

---

## 🤝 Contribuição

1. Fork o repositório  
2. Crie sua branch: `git checkout -b feature/nova-funcionalidade`  
3. Commit suas alterações: `git commit -m "Adiciona nova funcionalidade"`  
4. Push para a branch: `git push origin feature/nova-funcionalidade`  
5. Abra um Pull Request

