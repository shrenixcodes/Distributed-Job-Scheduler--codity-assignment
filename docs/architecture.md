
# Distributed Job Scheduler Architecture

## Overview
This is a production-grade distributed job scheduling system with the following components:

## Components

### Backend (FastAPI)
- RESTful API for managing users, organizations, projects, queues, and jobs
- JWT-based authentication
- Async database operations using SQLAlchemy and asyncpg

### Worker Service
- Polls queues for pending jobs
- Atomically claims jobs to prevent duplicate execution
- Executes jobs concurrently per queue's concurrency limit
- Sends heartbeats to track worker liveness

### Frontend (React + Vite)
- Responsive dashboard for monitoring and managing the system
- Real-time (polling) updates
- Visualization of job statistics with Recharts

### Database (PostgreSQL)
- Relational database for storing all system data
- JSONB support for flexible job payloads
- Indexes for performance optimization

## Job Lifecycle
1. **Queued**: Job is created and waiting to be processed
2. **Claimed**: Worker has claimed the job for processing
3. **Running**: Job is currently being executed
4. **Completed**: Job finished successfully
5. **Failed**: Job failed; may be retried based on retry policy
6. **Dead Letter**: Job exhausted all retries and moved to DLQ

## Tech Stack
- Backend: FastAPI, SQLAlchemy, asyncpg, Pydantic, python-jose
- Frontend: React, TypeScript, Vite, React Router, Axios, Recharts, Lucide React
- Database: PostgreSQL 15
- Containerization: Docker, Docker Compose
