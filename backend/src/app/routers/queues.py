
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.security import get_current_user
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
    result = await db.execute(select(Queue))
    return result.scalars().all()

@router.post("/{queue_id}/pause")
async def pause_queue(
    queue_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Queue).where(Queue.id == queue_id))
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
    result = await db.execute(select(Queue).where(Queue.id == queue_id))
    queue = result.scalar_one_or_none()
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")
    queue.is_paused = False
    await db.commit()
    return {"message": "Queue resumed"}
