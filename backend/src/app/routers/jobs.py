
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.job import Job, ScheduledJob
from ..models.organization import OrganizationMember
from ..models.project import Project
from ..models.queue import Queue
from ..models.user import User
from ..schemas.job import JobCreate, JobResponse, ScheduledJobCreate

router = APIRouter()

@router.post("/", response_model=JobResponse)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    queue_result = await db.execute(
        select(Queue.id)
        .join(Project, Queue.project_id == Project.id)
        .join(OrganizationMember, Project.organization_id == OrganizationMember.organization_id)
        .where(Queue.id == job.queue_id, OrganizationMember.user_id == current_user.id)
    )
    if queue_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Queue not found")

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
    query = (
        select(Job)
        .join(Queue, Job.queue_id == Queue.id)
        .join(Project, Queue.project_id == Project.id)
        .join(OrganizationMember, Project.organization_id == OrganizationMember.organization_id)
        .where(OrganizationMember.user_id == current_user.id)
        .order_by(Job.created_at.desc())
    )
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
    queue_result = await db.execute(
        select(Queue.id)
        .join(Project, Queue.project_id == Project.id)
        .join(OrganizationMember, Project.organization_id == OrganizationMember.organization_id)
        .where(Queue.id == job.queue_id, OrganizationMember.user_id == current_user.id)
    )
    if queue_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Queue not found")

    db_job = ScheduledJob(**job.model_dump())
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return {"message": "Scheduled job created", "id": db_job.id}
