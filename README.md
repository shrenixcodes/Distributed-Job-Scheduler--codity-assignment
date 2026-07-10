# Distributed Job Scheduler -codity assignment

## Overview
This repository implements a **production‑grade distributed job scheduling platform** as described in the academic assignment. It includes:
- **Backend** – FastAPI (Python) with JWT authentication, PostgreSQL, and a separate worker service.
- **Frontend** – React + Vite (TypeScript) dashboard with a modern, premium UI.
- **Database** – PostgreSQL schema and ER diagram.
- **Docker Compose** – Spins up PostgreSQL, backend, and frontend together.

## Quick Start
```powershell
# From the repository root
# Install Python deps (use a venv preferred)
python -m venv venv
.\venv\Scripts\activate
pip install -r backend/requirements.txt

# Install JS deps for frontend
cd frontend
npm install
cd ..

# Start everything (Docker must be installed & running)
# This will launch PostgreSQL, the FastAPI API, and the React UI
docker-compose up --build
```
- API docs: http://localhost:8000/docs
- UI: http://localhost:5173

## Project Structure
```
Distributed Job Scheduler -codity assignment/
├─ backend/                 # FastAPI service
│   ├─ src/
│   │   └─ app/
│   │       ├─ __init__.py
│   │       ├─ main.py
│   │       └─ routers/
│   │           ├─ __init__.py
│   │           ├─ auth.py
│   │           ├─ projects.py
│   │           ├─ queues.py
│   │           ├─ jobs.py
│   │           └─ workers.py
│   ├─ requirements.txt
│   └─ Dockerfile
├─ frontend/                # React Vite dashboard (generated)
├─ db/                      # Database schema & diagrams
│   ├─ schema.sql
│   └─ er_diagram.mmd
├─ docs/                    # Architecture & design docs (future)
├─ docker-compose.yml
├─ README.md                # This file
└─ .gitignore
```"
