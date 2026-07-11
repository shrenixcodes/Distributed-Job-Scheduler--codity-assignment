
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.organization import OrganizationMember
from ..models.project import Project
from ..models.queue import Queue, RetryPolicy
from ..models.user import User
from ..schemas.queue import QueueCreate, QueueResponse, RetryPolicyCreate

router = APIRouter()

@router.post("/", response_model=QueueResponse)
async def create_queue(
    queue: QueueCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project_result = await db.execute(
        select(Project.id)
        .join(OrganizationMember, Project.organization_id == OrganizationMember.organization_id)
        .where(Project.id == queue.project_id, OrganizationMember.user_id == current_user.id)
    )
    if project_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Project not found")

    db_queue = Queue(**queue.model_dump())
    db.add(db_queue)
    await db.commit()
    await db.refresh(db_queue)
    
    default_retry = RetryPolicy(queue_id=db_queue.id)
    db.add(default_retry)
    await db.commit()
    
    return db_queue

@router.get("/", response_model=list[QueueResponse])
async def get_queues(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Queue)
        .join(Project, Queue.project_id == Project.id)
        .join(OrganizationMember, Project.organization_id == OrganizationMember.organization_id)
        .where(OrganizationMember.user_id == current_user.id)
        .order_by(Queue.created_at.desc())
    )
    return result.scalars().all()

@router.post("/{queue_id}/pause")
async def pause_queue(
    queue_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Queue)
        .join(Project, Queue.project_id == Project.id)
        .join(OrganizationMember, Project.organization_id == OrganizationMember.organization_id)
        .where(Queue.id == queue_id, OrganizationMember.user_id == current_user.id)
    )
    queue = result.scalar_one_or_none()
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")
    queue.is_paused = True
    await db.commit()
    return {"message": "Queue paused"}

@router.post("/{queue_id}/resume")
async def resume_queue(
    queue_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Queue)
        .join(Project, Queue.project_id == Project.id)
        .join(OrganizationMember, Project.organization_id == OrganizationMember.organization_id)
        .where(Queue.id == queue_id, OrganizationMember.user_id == current_user.id)
    )
    queue = result.scalar_one_or_none()
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")
    queue.is_paused = False
    await db.commit()
    return {"message": "Queue resumed"}
