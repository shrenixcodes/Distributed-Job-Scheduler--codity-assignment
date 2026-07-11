
# Design Decisions

## 1. Database Choice: PostgreSQL
- **Why**: Strong relational model support, JSONB for flexible payloads, ACID compliance, excellent for job scheduling systems.
- **Trade-offs**: More complex than NoSQL options, but necessary for data integrity and relationships.

## 2. Backend Framework: FastAPI
- **Why**: Async support, automatic OpenAPI docs, Pydantic for validation, excellent performance.
- **Trade-offs**: Smaller ecosystem compared to Flask/Django, but sufficient for our needs.

## 3. ORM: SQLAlchemy 2.0 (Async)
- **Why**: Async support, powerful query building, ORM pattern for maintainability.
- **Trade-offs**: Learning curve for async patterns, but necessary for scalability.

## 4. Authentication: JWT
- **Why**: Stateless, scalable, easy to implement with FastAPI.
- **Trade-offs**: Token size, no built-in revocation (can be added with a token blacklist if needed).

## 5. Job Claiming: Atomic Database Updates
- **Why**: Prevents duplicate job execution by using database-level atomic operations.
- **Trade-offs**: Adds database load, but necessary for correctness.

## 6. Worker Liveness: Heartbeats
- **Why**: Allows detecting failed workers and requeuing their jobs.
- **Trade-offs**: Additional database writes, but necessary for reliability.

## 7. Frontend: React + Vite
- **Why**: Fast development, modern tooling, excellent TypeScript support.
- **Trade-offs**: Steeper learning curve than vanilla JS, but worth it for maintainability.
