
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.worker import Worker
from ..models.user import User
from ..schemas.worker import WorkerResponse

router = APIRouter()

@router.get("/", response_model=list[WorkerResponse])
async def get_workers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Worker))
    return result.scalars().all()
