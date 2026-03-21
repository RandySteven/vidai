# vidai

FastAPI service.

## Layout (MVC-style)

| Layer | Location | Role |
|--------|-----------|------|
| **Controller** | `app/controllers/v1/` | FastAPI routers: validate HTTP, call services, return response schemas |
| **Service** | `app/services/` | Use cases / orchestration |
| **Model** | `app/entities/models/` | Domain models (Pydantic) |
| **View (API)** | `app/entities/payloads/` | Request/response DTOs for JSON |
| **Repository** | `app/repositories/` | Persistence on top of `app/external/` |

`app/api/v1/router.py` mounts versioned controllers only.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cp app/toml/service-config.example.toml app/toml/service-config.local.toml
# Edit service-config.local.toml (gitignored): Atlas URI, Aiven MySQL/Redis, TLS flags.
# Or set VIDAI_SERVICE_CONFIG_PATH to another TOML file (e.g. in a mounted secret).
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health
