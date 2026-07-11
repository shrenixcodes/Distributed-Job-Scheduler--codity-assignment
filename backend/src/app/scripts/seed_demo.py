"""Create a presentation-ready XYZ App Build workspace.

Run from ``backend`` with:
    python -m src.app.scripts.seed_demo
"""

import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from ..core.database import AsyncSessionLocal, Base, engine
from ..core.security import get_password_hash
from ..models.job import Job
from ..models.organization import Organization, OrganizationMember
from ..models.project import Project
from ..models.queue import Queue, RetryPolicy
from ..models.user import User
from ..models.worker import Worker

DEMO_EMAIL = "demo@xyzbuild.dev"
DEMO_PASSWORD = "xyz-demo-2026"
PROJECT_NAME = "XYZ App Build"


async def get_or_create_demo_user(session) -> User:
    user = await session.scalar(select(User).where(User.email == DEMO_EMAIL))
    if user:
        return user

    user = User(
        email=DEMO_EMAIL,
        hashed_password=get_password_hash(DEMO_PASSWORD),
        full_name="XYZ Build Demo",
    )
    session.add(user)
    await session.flush()

    organization = Organization(name="XYZ Apps")
    session.add(organization)
    await session.flush()
    session.add(OrganizationMember(organization_id=organization.id, user_id=user.id, role="admin"))
    await session.flush()
    return user


async def get_demo_organization_id(session, user: User):
    return await session.scalar(
        select(OrganizationMember.organization_id).where(OrganizationMember.user_id == user.id).limit(1)
    )


async def seed() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as session:
        user = await get_or_create_demo_user(session)
        organization_id = await get_demo_organization_id(session, user)

        project = await session.scalar(
            select(Project).where(Project.organization_id == organization_id, Project.name == PROJECT_NAME)
        )
        if project is None:
            project = Project(
                organization_id=organization_id,
                name=PROJECT_NAME,
                description="Build, test, and deploy the XYZ customer application.",
            )
            session.add(project)
            await session.flush()

        queue_specs = [
            ("frontend-builds", "Compile the XYZ React application and publish build artifacts.", 10, 3),
            ("api-builds", "Package the Python API and run static checks.", 9, 2),
            ("quality-gates", "Run browser, API, and regression test suites.", 8, 4),
            ("preview-deploys", "Deploy validated builds to preview environments.", 6, 1),
            ("release-notifications", "Notify the team when releases are ready.", 4, 2),
        ]
        queues: dict[str, Queue] = {}
        for name, description, priority, concurrency_limit in queue_specs:
            queue = await session.scalar(
                select(Queue).where(Queue.project_id == project.id, Queue.name == name)
            )
            if queue is None:
                queue = Queue(
                    project_id=project.id,
                    name=name,
                    description=description,
                    priority=priority,
                    concurrency_limit=concurrency_limit,
                )
                session.add(queue)
                await session.flush()
                session.add(RetryPolicy(queue_id=queue.id, max_retries=3, strategy="exponential", delay_seconds=30))
            queues[name] = queue

        job_count = await session.scalar(
            select(func.count()).select_from(Job).join(Queue, Job.queue_id == Queue.id).where(Queue.project_id == project.id)
        )
        if job_count == 0:
            jobs = [
                Job(queue_id=queues["frontend-builds"].id, status="queued", priority=10, scheduled_at=now + timedelta(hours=1), created_at=now - timedelta(minutes=2), payload={"app": "xyz-web", "branch": "feature/checkout", "commit": "a17c9d2", "task": "vite-production-build"}),
                Job(queue_id=queues["frontend-builds"].id, status="completed", priority=9, started_at=now - timedelta(minutes=27), completed_at=now - timedelta(minutes=23), created_at=now - timedelta(minutes=28), payload={"app": "xyz-web", "branch": "main", "commit": "8f3a19c", "task": "bundle-dashboard"}),
                Job(queue_id=queues["api-builds"].id, status="queued", priority=9, scheduled_at=now + timedelta(minutes=45), created_at=now - timedelta(minutes=4), payload={"app": "xyz-api", "branch": "release/2.4", "commit": "c4e1f77", "task": "package-api-image"}),
                Job(queue_id=queues["quality-gates"].id, status="failed", priority=8, started_at=now - timedelta(minutes=19), failed_at=now - timedelta(minutes=14), created_at=now - timedelta(minutes=20), retry_count=1, payload={"app": "xyz-web", "suite": "checkout-regression", "task": "playwright-tests", "error": "Expected payment confirmation"}),
                Job(queue_id=queues["quality-gates"].id, status="completed", priority=8, started_at=now - timedelta(minutes=40), completed_at=now - timedelta(minutes=32), created_at=now - timedelta(minutes=41), payload={"app": "xyz-api", "suite": "contract-tests", "task": "run-api-tests"}),
                Job(queue_id=queues["preview-deploys"].id, status="running", priority=6, started_at=now - timedelta(minutes=6), created_at=now - timedelta(minutes=7), payload={"app": "xyz-web", "environment": "preview-pr-482", "task": "deploy-preview"}),
                Job(queue_id=queues["release-notifications"].id, status="completed", priority=4, started_at=now - timedelta(minutes=55), completed_at=now - timedelta(minutes=54), created_at=now - timedelta(minutes=56), payload={"app": "xyz-api", "release": "v2.3.1", "channel": "engineering", "task": "announce-release"}),
            ]
            session.add_all(jobs)

        for name, status in [("xyz-build-agent-us-east", "running"), ("xyz-quality-runner-02", "idle"), ("xyz-preview-deployer", "idle")]:
            worker = await session.scalar(select(Worker).where(Worker.name == name))
            if worker is None:
                session.add(Worker(name=name, status=status, last_heartbeat=now))
            else:
                worker.status = status
                worker.last_heartbeat = now

        await session.commit()

    print(f"Demo workspace is ready. Sign in with {DEMO_EMAIL} / {DEMO_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed())
