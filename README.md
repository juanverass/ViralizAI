# ViralizAI 🚀

**ViralizAI** é uma plataforma em Python para **criação automatizada de vídeos curtos (TikTok / YouTube Shorts)** usando IA. O sistema gera vídeos, dublagens e legendas automaticamente, podendo processar conteúdos via links ou prompts de texto.

---

## 🌟 Funcionalidades

- Criação de vídeos a partir de **prompts ou links de vídeos**.
- **Dublagem automática** (via ElevenLabs API).
- **Geração automática de legendas**.
- Integração com **n8n** para workflows automatizados.

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

## 🚀 Como Começar

1. Clone o repositório:

```bash
git clone <repo-url>
cd ViralizAI
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Rode a aplicação:

```bash
python -m uvicorn app.main:app --reload
```

---

## 🤝 Contribuição

Antes de mais nada, clique [AQUI](CONTRIBUTING.md) para ter informações sobre 
a nossa arquitetura e como pode ser criada uma nova funcionalidade do **zero**.

1. Fork o repositório
2. Crie branch: `git checkout -b feature/nova-funcionalidade`
3. Commit alterações: `git commit -m "Adiciona nova funcionalidade"`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra Pull Request

