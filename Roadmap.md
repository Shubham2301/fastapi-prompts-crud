# FastAPI Prompt Management API — Learning Roadmap

> Production-quality REST API built as a learning project.

## Project Goal

Build a production-quality Prompt Management REST API using FastAPI while learning backend engineering concepts hands-on.

The project should follow a clean layered architecture:

```text
Router → Service → Repository → PostgreSQL
```

Use this project to understand **why** each architectural decision is made, not just how to implement it.

---

# Roadmap

## Phase 1 — FastAPI Fundamentals ✅ DONE

- [x] Project setup
- [x] Python virtual environment (`venv`)
- [x] FastAPI + Uvicorn
- [x] First endpoint
- [x] Routing
- [x] Path parameters
- [x] Query parameters
- [x] Request bodies
- [x] Pydantic schemas & validation
- [x] Swagger / OpenAPI

**Status:** ✅ Complete

---



## Phase 2 — CRUD API ✅ DONE

- [x] Design Prompt resource
- [x] `POST /prompts`
- [x] `GET /prompts`
- [x] `GET /prompts/{id}`
- [x] `PUT /prompts/{id}`
- [x] `PATCH /prompts/{id}`
- [x] `DELETE /prompts/{id}`
- [x] PUT vs PATCH
- [x] HTTP status codes
- [x] Request schemas
- [x] Basic response schemas

**Status:** ✅ Complete

---



## Phase 3 — PostgreSQL + SQLAlchemy ✅ DONE

- [x] PostgreSQL with Docker
- [x] Connect using TablePlus
- [x] SQL vs NoSQL decision
- [x] SQLAlchemy setup
- [x] Database connection
- [x] SQLAlchemy models
- [x] Prompt table
- [x] Sessions
- [x] Alembic
- [x] Migrations
- [x] CRUD with PostgreSQL

**Status:** ✅ Complete

---



## Phase 4 — Application Architecture ✅ DONE

- [x] Separate schemas
- [x] Router layer
- [x] Service layer
- [x] Repository layer
- [x] Apply architecture to CRUD
- [x] Dependency injection
- [x] Custom exceptions
- [x] Global exception handlers
- [x] Business logic in Service layer
- [x] Database logic in Repository layer

**Status:** ✅ Complete

Architecture:

```text
Router → Service → Repository → PostgreSQL
```

---



## Phase 5 — Automated Testing ⏸️ SKIPPED FOR NOW

Learn testing fundamentals using pytest.

- [x] Install/configure pytest
- [ ] First test
- [ ] Schema tests
- [ ] Exception tests
- [ ] Service unit tests
- [ ] Mocking
- [ ] Mock repositories
- [ ] FastAPI `TestClient`
- [ ] API success/error tests
- [ ] Isolated test database
- [ ] Repository integration tests
- [ ] Complete CRUD test suite

**Status:** ⏸️ Skipped — resume after Phase 6
**Note:** `pytest` is in `requirements.txt`. There are no test files yet. Earlier checkboxes for first/schema/exception tests did not match the repo.

Important concepts:

- Unit tests
- Integration tests
- Fixtures
- Mocking
- Dependency overrides
- Test database

---



## Phase 6 — Production API Quality ✅ DONE

- [x] Configuration management
- [x] Environment variables
- [x] `.env`
- [x] Logging
- [x] Consistent error responses
- [x] Pagination
- [x] Filtering & search
- [x] Sorting
- [x] API versioning
- [x] Health checks

**Status:** ✅ Complete

`Settings` lives in `app/core/config.py`. Prompt routes live under `/api/v1`. List supports `limit`/`offset`, `category`, `q`, `sort_by`/`sort_order`. `GET /health` is unversioned: 200 `{"status":"OK"}` when Postgres answers `SELECT 1`, 503 `SERVICE_UNAVAILABLE` if it does not.

---



## Phase 7 — Authentication & Authorization ⏸️ SKIPPED FOR NOW

- [ ] User model
- [ ] User registration
- [ ] Password hashing
- [ ] JWT authentication
- [ ] Login endpoint
- [ ] Protected routes
- [ ] User-specific prompts
- [ ] Authorization rules

**Status:** ⏸️ Skipped — resume after Phase 9

---



## Phase 8 — Prompt Management ⏸️ SKIPPED FOR NOW

- [ ] Prompt versions
- [ ] Tags
- [ ] Categories
- [ ] Search
- [ ] Prompt duplication
- [ ] Favorites
- [ ] Usage statistics
- [ ] Soft deletion

**Status:** ⏸️ Skipped — resume after Phase 9

---



## Phase 9 — AI Integration 🟡 IN PROGRESS

- [x] OpenAI-compatible API
- [x] Ollama
- [x] Prompt execution
- [ ] Execution history
- [ ] Token/cost tracking
- [ ] Model selection
- [ ] Streaming
- [ ] Embeddings

**Status:** 🟡 In Progress
**Current:** Execution history (9.3)

`POST /api/v1/prompts/{id}/execute` loads saved `Prompt.content`, POSTs OpenAI-compat chat to Ollama, returns `{prompt_id, model, output, usage}`. No extra user message. 404 if missing prompt; 503 if Ollama is down.

---



## Phase 10 — RAG / AI Knowledge ⬜ NOT STARTED

- [ ] Embeddings
- [ ] Vector database
- [ ] Semantic search
- [ ] Document ingestion
- [ ] Chunking
- [ ] Retrieval
- [ ] RAG pipeline
- [ ] Prompt + context

**Status:** ⬜ Not Started

---



## Phase 11 — Production & Deployment ⬜ NOT STARTED

- [ ] Dockerize FastAPI
- [ ] Docker Compose
- [ ] Production configuration
- [ ] Database migrations
- [ ] CI/CD
- [ ] Monitoring
- [ ] AWS deployment

**Status:** ⬜ Not Started

---



# Learning Rules

When working on this project:

1. **Understand WHY before implementing HOW.**
2. Keep the architecture:

```text
Router → Service → Repository
```

3. Don't put business logic in routers.
4. Don't put business logic in repositories.
5. Don't access the database directly from routers.
6. Use Pydantic for request/response contracts.
7. Write tests for new behavior.
8. Prefer incremental changes over large refactors.
9. Explain trade-offs before introducing new technologies.
10. Don't introduce abstractions unless they solve an actual problem.

---



# Current Position

**Phase 9 — AI Integration**

**Next:** Execution history (9.3)

```text
Phase 1  — FastAPI Fundamentals          ✅
Phase 2  — CRUD API                      ✅
Phase 3  — PostgreSQL + SQLAlchemy       ✅
Phase 4  — Application Architecture      ✅
Phase 5  — Automated Testing             ⏸️ SKIPPED
Phase 6  — Production API Quality        ✅
Phase 7  — Authentication & Authorization ⏸️ SKIPPED
Phase 8  — Prompt Management             ⏸️ SKIPPED
Phase 9  — AI Integration                🟡 CURRENT
Phase 10 — RAG / AI Knowledge            ⬜
Phase 11 — Production & Deployment       ⬜
```

---



# How to Use This With Cursor

Before making changes, read `Roadmap.md` and identify the current phase.

When asked to implement the next phase:

1. Explain the concept.
2. Explain WHY it is needed.
3. Inspect the existing implementation.
4. Make the smallest appropriate change.
5. Preserve the Router → Service → Repository architecture.
6. Add/update tests.
7. Explain what changed.
8. Update the roadmap status only when the step is actually completed.

Do not jump ahead to later phases unless explicitly requested.