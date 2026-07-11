
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.job import Job, ScheduledJob
from ..models.user import User
from ..schemas.job import JobCreate, JobResponse, ScheduledJobCreate

router = APIRouter()

@router.post("/", response_model=JobResponse)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_job = Job(**job.model_dump())
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

@router.get("/", response_model=list[JobResponse])
async def get_jobs(
    queue_id: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Job)
    if queue_id:
        query = query.where(Job.queue_id == queue_id)
    if status:
        query = query.where(Job.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/scheduled", response_model=dict)
async def create_scheduled_job(
    job: ScheduledJobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_job = ScheduledJob(**job.model_dump())
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return {"message": "Scheduled job created", "id": db_job.id}
