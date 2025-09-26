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

Este tutorial serve como guia completo para entender como o CRUD de qualquer entidade funciona na arquitetura hexagonal do projeto, camada por camada. Ele é pensado para desenvolvedores juniores ou qualquer pessoa que entre no projeto, garantindo clareza sobre responsabilidades, fluxo de dados e boas práticas. No exemplo a seguir utilizaremos a entidade **Video**.

### 1️⃣ **Criar a Entidade de Domínio**

> **🎯 Objetivo**: Criar a entidade que representa o conceito de negócio no domínio.

A entidade de domínio é o coração da aplicação. Ela contém:
- **Dados**: Propriedades da entidade
- **Regras**: Validações e comportamentos
- **Enums**: Estados possíveis
- **Factory Methods**: Métodos para criar instâncias

Crie o arquivo `domain/entities/videos/video.py`:

```python
@dataclass
class Video:
    id: str
    title: str
    source_url: str
    local_path: Optional[str] = None
    status: StatusDoVideo = StatusDoVideo.PENDENTE
```
**O que você está fazendo:**
- Está definindo o que é um vídeo no seu sistema, com seus atributos principais.
- id, title, source_url são dados que importam para você identificar e trabalhar com o vídeo.
- status indica se o vídeo está processando, pronto ou falhou.
- Por que é importante: isso é a "regra do negócio". O restante da aplicação deve usar isso, não o banco ou DTOs.

Resumo: A entidade **não depende de nada externo**, só do seu conceito de vídeo.


### 2️⃣ **Criar o Mapeamento de Banco (Modelo ORM)**

> **🎯 Objetivo**: Criar a representação da entidade no banco de dados.

O mapeamento de banco é responsável por:
- **Estrutura**: Definir como a entidade é armazenada no banco
- **Tipos**: Mapear tipos Python para tipos SQL
- **Constraints**: Definir regras de integridade (unique, nullable, etc.)
- **Relacionamentos**: Chaves estrangeiras e associações

> **⚠️ Importante**: Esta camada está na **Infrastructure** porque depende de tecnologia específica (SQLAlchemy).

Crie o arquivo `infrastructure/models/videos/video_db_mapping.py`:

```python
class VideoDbMapping(Base):
    id = Column(String(36), primary_key=True)
    title = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    status = Column(Enum(StatusDoVideo), default=StatusDoVideo.PENDENTE)

```
**O que você está fazendo:**

- Está definindo como esse vídeo vai ser salvo no banco de dados.
- Aqui você diz que id é uma chave primária, title é obrigatório, etc.
- **Por que é separado:** se você mudar de banco, **não precisa mudar a entidade**

### 3️⃣ **Criar o Mapper (esse passo confunde a maioria)**

> **🎯 Objetivo**: Criar a ponte entre a entidade de domínio e o mapeamento de banco.

O mapper é responsável por:
- **Conversão**: Transformar entidade ↔ model de banco
- **Isolamento**: Manter domínio independente da tecnologia de persistência
- **Mapeamento**: Garantir que todos os campos sejam convertidos corretamente
- **Bidirecional**: Funciona nos dois sentidos (to_model e to_entity)

> **💡 Por que precisamos do Mapper?**
>
> - A entidade (Video) é a forma como pensamos no negócio.
> - O modelo ORM (VideoDbMapping) é a forma como o banco entende.
> - O Mapper é o tradutor entre essas duas formas. Ele pega um vídeo do domínio e transforma em algo que o banco entende, ou pega um registro do banco e transforma de volta em uma entidade que a aplicação entende.

> **to_model**
>
> - Entrada: Entidade (Video)
> - Saída: Modelo ORM (VideoDbMapping)
> - Exemplo prático: você quer salvar um vídeo no banco.
>    - Você tem o vídeo no formato do domínio.
>    - to_model pega ele e cria um objeto que SQLAlchemy sabe salvar.

> **to_entity**
>
> - Entrada: Modelo ORM (VideoDbMapping)
> - Saída: Entidade (Video)
> - Exemplo prático: você acabou de buscar um vídeo no banco.
>    - SQLAlchemy te dá um VideoDbMapping.
>    - to_entity transforma em Video para a aplicação usar sem se preocupar com SQL.

> **Resumo simples:** Mapper = tradutor entre o “idioma” do negócio e o “idioma” do banco.
> - Sem ele, você teria que colocar lógica de banco dentro do seu domínio ou lógica de negócio dentro do SQLAlchemy.
> - Isso mistura responsabilidades e é ruim para manutenção. 

> O domínio não deve conhecer detalhes de implementação. O mapper permite que:
> - A entidade permaneça "pura" (sem dependências de SQLAlchemy)
> - Possamos trocar de ORM sem afetar o domínio
> - O código seja mais testável e flexível

Crie o arquivo `infrastructure/mappers/videos/video_persistence_mapper.py`:

```python
class VideoPersistenceMapper:
    @staticmethod
    def to_model(entity: Video) -> VideoDbMapping:
        return VideoDbMapping(
            id=entity.id,
            title=entity.title,
            source_url=entity.source_url,
            status=entity.status
        )

    @staticmethod
    def to_entity(model: VideoDbMapping) -> Video:
        return Video(
            id=model.id,
            title=model.title,
            source_url=model.source_url,
            status=model.status
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

Crie o arquivo `domain/repositories/video_repository_port.py`:

```python
class VideoRepositoryPort(BaseRepositoryPort[Video]):
    """Contrato para repositório de vídeos"""  
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
> ├── BaseRepository[Video, VideoDbMapping]  # CRUD genérico
> └── VideoRepository                       # Contrato do domínio
> ```
> 
> **Benefícios:**
> - **CRUD automático**: Herda operações básicas do BaseRepository
> - **Type Safety**: Type hints garantem tipos corretos
> - **Flexibilidade**: Pode adicionar métodos específicos
> - **Testabilidade**: Fácil de mockar para testes

Crie o arquivo `infrastructure/repositories/videos/video_repository.py`:

```python
class VideoRepository(BaseRepository[Video, VideoDbMapping], VideoRepositoryPort):
    """Implementação do repositório de vídeos usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        super().__init__(session, VideoDbMapping, VideoPersistenceMapper)
    
    # ❌ NÃO coloque métodos específicos de negócio aqui!
    # O Repository deve ser genérico e focado apenas em persistência
    # Métodos como update_status() pertencem ao Service
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
> VideoService
> ├── BaseAppService[Video]           # CRUD padrão herdado
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

> **⚠️ Separação de Responsabilidades:**
> 
> **Repository (Infrastructure):**
> - ✅ Operações genéricas de persistência (CRUD)
> - ✅ Conversão entre entidade e model
> - ❌ Regras de negócio específicas
> - ❌ Validações de domínio
> 
> **Service (Application):**
> - ✅ Regras de negócio e validações
> - ✅ Orquestração de operações
> - ✅ Casos de uso específicos
> - ✅ Aplicação de regras antes de persistir

Crie o arquivo `app/services/videos/video_service.py`:

```python
class VideoService(BaseAppService[Video]):
    """Serviço de vídeos - casos de uso específicos do domínio"""
    
    def __init__(self, repository: _repository):
        super().__init__(repository)

    def create_video(self, title: str, source_url: str) -> Video:
        """Cria um novo vídeo"""
        video = Video.create_new(title, source_url)
        return  _repository.add(video)
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

Crie o arquivo `interfaces/api/schemas/video_schemas.py`:

```python
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

    class Config:
        from_attributes = True

```

### 8️⃣ **Criar o Controller**

> **🎯 Objetivo**: Criar os endpoints REST que expõem a funcionalidade via HTTP.

O Controller é responsável por:
- **Endpoints**: Definir rotas HTTP (GET, POST, PUT, DELETE)
- **Validação**: Usar schemas Pydantic para validar entrada
- **Tratamento**: Converter erros de domínio em respostas HTTP
- **Documentação**: Gerar documentação automática (Swagger)

> **🏗️ Estrutura do Controller:**
> 
> ```
> VideoController
> ├── Endpoints CRUD padrão        # GET, POST, PUT, DELETE
> ├── Validação de entrada         # Schemas Pydantic
> ├── Tratamento de erros         # HTTPException
> └── Injeção de dependência      # Service via FastAPI Depends
> ```

> **💡 Padrões de Endpoint:**
> 
> - **POST /usuarios**: Criar novo video
> - **GET /usuarios**: Listar todos os videos
> - **GET /usuarios/{id}**: Buscar video específico
> - **PUT /usuarios/{id}**: Atualizar video completo
> - **DELETE /usuarios/{id}**: Remover video

> **🔧 Injeção de Dependência:**
> 
> O FastAPI usa `Depends()` para injetar o service automaticamente:
> - **Testabilidade**: Fácil de mockar em testes
> - **Reutilização**: Mesmo service usado em múltiplos endpoints
> - **Configuração**: Centralizada no `main.py`

Crie o arquivo `interfaces/api/video_controller.py`:

```python
router = APIRouter()

def get_services(request: Request) -> ServiceRegistrationBlock:
    return request.app.state.services

def get_video_service(services: ServiceRegistrationBlock = Depends(get_services)) -> VideoService:
    return services.video_service

# ===== HERANÇA DO BASE CONTROLLER =====
class VideoController(BaseController[Video, VideoService]):
    """Controller de vídeos com herança do BaseController"""
    
    def __init__(self):
        super().__init__(router, get_video_service(), "Vídeo")
        self._register_specific_routes()
    
    def _register_specific_routes(self):
        """Registra rotas específicas do domínio de vídeos"""
        
        @self.router.post("", response_model=VideoResponse)
        def create_video(
            video_data: VideoCreateRequest,
            video_service: VideoService = Depends(get_video_service)
        ):
            """Cria um novo vídeo"""
            return video_service.create_video(video_data.title, video_data.source_url)
        
        @self.router.patch("/{video_id}/mark-processing", response_model=VideoResponse)
        def mark_processing(
            video_id: str,
            video_service: VideoService = Depends(get_video_service)
        ):
            """Marca vídeo como processando"""
            video = video_service.mark_processing(video_id)
            if not video:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vídeo não encontrado"
                )
            return video

        @self.router.patch("/{video_id}/mark-ready", response_model=VideoResponse)
        def mark_ready(
            video_id: str,
            video_service: VideoService = Depends(get_video_service)
        ):
            """Marca vídeo como pronto"""
            video = video_service.mark_ready(video_id)
            if not video:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vídeo não encontrado"
                )
            return video

        @self.router.patch("/{video_id}/mark-failed", response_model=VideoResponse)
        def mark_failed(
            video_id: str,
            video_service: VideoService = Depends(get_video_service)
        ):
            """Marca vídeo como falhou"""
            video = video_service.mark_failed(video_id)
            if not video:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vídeo não encontrado"
                )
            return video

# Instanciar o controller para registrar as rotas
video_controller = VideoController()
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
class RepositoryRegistrationBlock:
    def __init__(self, session):
        self.videos = VideoRepository(session)
```

**ServiceRegistrationBlock** (`app/services/service_registration_block.py`):
```python 
class ServiceRegistrationBlock:
    def __init__(self, repositories: RepositoryRegistrationBlock):
        self.video_service = VideoService(repositories.videos)
        self.usuario_service = UsuarioService(repositories.usuarios)
```

**RouterRegistrationBlock** (`interfaces/api/router_registration_block.py`):
```python 
class RouterRegistrationBlock:
    def __init__(self):
        self.routers = [
            (video_controller.router, "/videos", ["Vídeos"]),
        ]

    def register_all(self, app: FastAPI):
        for router, prefix, tags in self.routers:
            app.include_router(router, prefix=prefix, tags=tags)
```

### ✅ **Resultado Final**

Após seguir este tutorial, você terá:

- **Entidade**: `Video` com regras de domínio
- **Mapeamento**: `VideoDbMapping` para persistência
- **Repository**: `VideoRepository` com CRUD completo
- **Service**: `VideoService` com casos de uso
- **Controller**: Endpoints REST completos
- **Schemas**: Validação de entrada/saída

**Endpoints disponíveis:**
- `POST /videos` - Criar usuário
- `GET /videos` - Listar todos
- `GET /videos/{id}` - Buscar por ID
- `PUT /videos/{id}/block` - Bloquear usuário
- `PUT /videos/{id}/activate` - Ativar usuário

---

## 🎓 **Resumo da Arquitetura Hexagonal**

### **📋 Camadas e Responsabilidades:**

| Camada | Responsabilidade | Exemplo |
|--------|------------------|---------|
| **Domain** | Regras de negócio puras | `Video`, `StatusDoVideo`, `VideoRepositoryPort` |
| **Application** | Casos de uso e orquestração | `VideoService` |
| **Infrastructure** | Implementações técnicas | `VideoRepository`, `Video`, `VideoPersistenceMapper` |
| **Interfaces** | Pontos de entrada | `VideoController`, `VideoSchemas` |

### **🔄 Fluxo de Dados:**

```
HTTP Request → Controller → Service → Repository → Database
                                                       ↓
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

## 🎯 **Boas Práticas e Padrões**

### **📋 Onde Colocar Cada Tipo de Código:**

| **Código** | **Onde Colocar** | **Por quê** |
|------------|------------------|-------------|
| **Regras de negócio** | Service | Orquestração e validação |
| **Validações de domínio** | Service | Aplicação de regras antes de persistir |
| **Operações CRUD** | Repository | Persistência genérica |
| **Conversões de dados** | Mapper | Isolamento entre camadas |
| **Endpoints HTTP** | Controller | Interface com o mundo externo |
| **Validação de entrada** | Schemas | Validação de dados da API |

### **❌ Erros Comuns a Evitar:**

```python
# ❌ ERRADO: Repository com regras de negócio
class UsuarioRepository:
    def block_usuario(self, id):  # Regra de negócio no Repository
        usuario = self.get_by_id(id)
        if usuario.status == "ATIVO":  # Validação no Repository
            usuario.status = "BLOQUEADO"
            return self.update(usuario)

# ✅ CORRETO: Service com regras de negócio
class UsuarioService:
    def block_usuario(self, id):
        usuario = self.get_by_id(id)
        if not usuario:
            return None
        
        # Validação de negócio no Service
        if usuario.status != StatusUsuario.ATIVO:
            raise ValueError("Apenas usuários ativos podem ser bloqueados")
        
        usuario.status = StatusUsuario.BLOQUEADO
        return self.update(usuario)  # Usa Repository genérico
```

### **💡 Princípios da Arquitetura Hexagonal:**

1. **Dependency Inversion**: Dependências apontam para o domínio
2. **Single Responsibility**: Cada classe tem uma responsabilidade
3. **Interface Segregation**: Interfaces específicas e focadas
4. **Open/Closed**: Aberto para extensão, fechado para modificação

### **🎯 Padrão de Controller com Herança:**

```python
# ✅ CORRETO: Controller com herança real do BaseController
class EntityController(BaseController[Entity, EntityService]):
    """Controller com herança do BaseController"""
    
    def __init__(self):
        super().__init__(router, get_entity_service(), "Entidade")
        self._register_specific_routes()
    
    def _register_specific_routes(self):
        """Registra rotas específicas do domínio"""
        
        @self.router.post("", response_model=EntityResponse)
        def create_entity(data: CreateRequest, service: EntityService = Depends(get_service)):
            return service.create_entity(data.field1, data.field2)

        @self.router.patch("/{id}/specific-action", response_model=EntityResponse)
        def specific_action(id: str, service: EntityService = Depends(get_service)):
            return service.specific_business_action(id)

# Instanciar para registrar as rotas
entity_controller = EntityController()
```

**Endpoints automáticos (herdados do BaseController):**
- `GET /entities` - Listar todos
- `GET /entities/{id}` - Buscar por ID
- `PUT /entities/{id}` - Atualizar
- `DELETE /entities/{id}` - Remover

**Endpoints específicos (registrados manualmente):**
- `POST /entities` - Criar entidade
- `PATCH /entities/{id}/specific-action` - Ação específica

**Benefícios desta abordagem:**
- **Herança Real**: CRUD automático via BaseController
- **Especialização**: Rotas específicas do domínio
- **Reutilização**: Aproveita toda a funcionalidade base
- **Manutenção**: Mudanças no BaseController afetam todos os controllers
- **Organização**: Código limpo e bem estruturado

---

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

