from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, projects, queues, jobs, workers

app = FastAPI(title="Distributed Job Scheduler API", version="0.1.0")

# CORS configuration (allow all for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(queues.router, prefix="/api/queues", tags=["queues"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(workers.router, prefix="/api/workers", tags=["workers"])

@app.get("/")
async def root():
    return {"message": "Distributed Job Scheduler API is running"}
