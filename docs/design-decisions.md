
# Design Decisions & Trade-offs

## 1. Database Selection
- **PostgreSQL (Prod)**: ACID compliance, JSONB support, mature for job scheduling
- **SQLite (Dev)**: Easy to set up, no external dependencies, great for rapid prototyping
- **Trade-off**: SQLite lacks concurrency for multi-worker setups, so use PostgreSQL for any production-like testing

## 2. Async vs Sync Backend
- **Chose Async (FastAPI + SQLAlchemy 2.0)**: Better throughput for I/O-bound tasks (DB calls, job scheduling)
- **Trade-off**: Slightly more complex code, but worth it for scalability

## 3. Job Claiming
- **Atomic DB Operation**: Use DB-level transactions to ensure only one worker claims a job
- **Why Not Distributed Locks (Redis)**: Keeps initial architecture simple; can add Redis later if needed
- **Trade-off**: Tighter coupling to DB, but avoids introducing another service

## 4. Password Hashing
- **bcrypt via passlib**: Slow hashing algorithm resistant to brute-force attacks
- **Why Not Argon2?**: bcrypt is more widely supported and still very secure for this use case

## 5. JWT for Auth
- **Stateless Auth**: No server-side session storage; easy to scale horizontally
- **Trade-off**: Tokens can't be revoked easily without a token blacklist (future improvement)

## 6. Frontend State Management
- **Local State (useState/useEffect)**: Simple for initial version; avoids over-engineering
- **Future**: Could add React Query or SWR for better caching

## 7. Worker Implementation
- **Polling (Simple)**: Workers periodically check queues for jobs
- **Alternative**: Event-driven (Redis Pub/Sub, Postgres NOTIFY/LISTEN) for lower latency
- **Trade-off**: Polling has slight latency, but is simple and reliable

## 8. Containerization
- **Docker Compose**: Orchestrates backend, worker, frontend, and DB in one command
- **Why Not Kubernetes?**: Overkill for this scope, but easy to migrate later

