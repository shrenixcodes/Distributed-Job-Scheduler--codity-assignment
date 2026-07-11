
# Distributed Job Scheduler

## Overview
Production-ready distributed job scheduling system built with FastAPI, PostgreSQL (or SQLite for dev), and React. Supports priority queues, retries, dead letter queues, and more.

## System Design Highlights
1. **Authentication & Authorization**: JWT-based auth with user and organization management
2. **Queueing System**: Priority-based queues with concurrency limits, pause/resume functionality
3. **Job Lifecycle**: Queued → Scheduled → Claimed → Running → Completed/Failed
4. **Reliability**: Retry policies (fixed, linear, exponential), dead letter queue
5. **Workers**: Worker heartbeat monitoring, graceful shutdown support
6. **Scheduling**: Immediate, delayed, and cron-based scheduled jobs

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy 2.0 (async), Pydantic
- **Database**: PostgreSQL (prod) / SQLite (dev)
- **Frontend**: React, TypeScript, Vite, Recharts, Lucide Icons
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, pytest-asyncio, httpx

## Quick Start

### Local Development
#### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
# Run server
uvicorn app.main:app --reload
```
Backend API will be at http://127.0.0.1:8000

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will be at http://localhost:5173

### Docker Setup
```bash
docker-compose up --build
```

## Project Structure
```
Distributed Job Scheduler -codity assignment/
├── backend/
│   ├── src/
│   │   └── app/
│   │       ├── core/          # Config, db setup, security
│   │       ├── models/        # SQLAlchemy models
│   │       ├── schemas/       # Pydantic schemas
│   │       ├── routers/       # API endpoints
│   │       ├── services/      # Worker service
│   │       └── main.py        # FastAPI app
│   ├── tests/                 # pytest tests
│   └── Dockerfile
├── frontend/                  # React app
├── db/                        # Database init scripts
├── docs/                      # Architecture & design docs
├── docker-compose.yml
└── README.md
```

## API Endpoints
All endpoints (except auth) require a Bearer token from `/api/auth/login`.

### Auth
| Method | Endpoint          | Description               |
|--------|-------------------|---------------------------|
| POST   | /api/auth/register| Create new user           |
| POST   | /api/auth/login   | Get JWT access token      |

### Projects
| Method | Endpoint           | Description               |
|--------|--------------------|---------------------------|
| GET    | /api/projects      | List all projects         |
| POST   | /api/projects      | Create new project        |

### Queues
| Method | Endpoint                | Description               |
|--------|-------------------------|---------------------------|
| GET    | /api/queues             | List all queues           |
| POST   | /api/queues             | Create new queue          |
| POST   | /api/queues/{id}/pause  | Pause a queue             |
| POST   | /api/queues/{id}/resume | Resume a queue            |

### Jobs
| Method | Endpoint           | Description               |
|--------|--------------------|---------------------------|
| GET    | /api/jobs          | List jobs (filterable)    |
| POST   | /api/jobs          | Create new job            |
| POST   | /api/jobs/scheduled| Create scheduled job      |

### Workers
| Method | Endpoint           | Description               |
|--------|--------------------|---------------------------|
| GET    | /api/workers       | List all workers          |

## Design & Documentation
- [Architecture Overview](docs/architecture.md)
- [Design Decisions & Trade-offs](docs/design-decisions.md)
- [ER Diagram](db/er-diagram.md) (to be created)

## Testing
```bash
cd backend
pytest
```

## Interview Talking Points
1. **Database Design**: Normalized schema for users, orgs, projects, queues, jobs
2. **Atomic Job Claiming**: Prevent duplicate job execution
3. **Retry Policies**: Configurable strategies with backoff
4. **Worker Heartbeats**: Monitor worker health for failover
5. **Async Operations**: High-throughput with async SQLAlchemy
6. **Security**: JWT auth, password hashing with bcrypt

