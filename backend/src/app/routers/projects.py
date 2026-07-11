
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..core.security import get_current_organization_id, get_current_user
from ..models.organization import OrganizationMember
from ..models.project import Project
from ..models.user import User
from ..schemas.project import ProjectCreate, ProjectResponse

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    organization_id = project.organization_id or await get_current_organization_id(current_user, db)
    membership = await db.execute(
        select(OrganizationMember.id).where(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    if membership.scalar_one_or_none() is None:
        raise HTTPException(status_code=403, detail="You do not have access to this organization")

    db_project = Project(
        name=project.name,
        description=project.description,
        organization_id=organization_id,
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("/", response_model=list[ProjectResponse])
async def get_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project)
        .join(OrganizationMember, Project.organization_id == OrganizationMember.organization_id)
        .where(OrganizationMember.user_id == current_user.id)
        .order_by(Project.created_at.desc())
    )
    return result.scalars().all()
