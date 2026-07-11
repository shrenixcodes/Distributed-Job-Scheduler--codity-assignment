
import asyncio
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from ..core.database import AsyncSessionLocal
from ..models.queue import Queue
from ..models.job import Job, JobExecution
from ..models.worker import Worker, WorkerHeartbeat

class JobWorker:
    def __init__(self, name: str = None):
        self.worker_id = uuid.uuid4()
        self.name = name or f"worker-{self.worker_id}"
        self.running = False

    async def start(self):
        self.running = True
        print(f"Worker {self.name} starting...")
        
        async with AsyncSessionLocal() as db:
            worker = Worker(id=self.worker_id, name=self.name, status="idle")
            db.add(worker)
            await db.commit()
        
        await asyncio.gather(
            self.poll_jobs(),
            self.send_heartbeats()
        )

    async def stop(self):
        self.running = False

    async def poll_jobs(self):
        while self.running:
            try:
                await self.claim_and_execute_jobs()
            except Exception as e:
                print(f"Error polling jobs: {e}")
            await asyncio.sleep(1)

    async def send_heartbeats(self):
        while self.running:
            try:
                async with AsyncSessionLocal() as db:
                    await db.execute(
                        update(Worker)
                        .where(Worker.id == self.worker_id)
                        .values(last_heartbeat=datetime.utcnow())
                    )
                    heartbeat = WorkerHeartbeat(worker_id=self.worker_id)
                    db.add(heartbeat)
                    await db.commit()
            except Exception as e:
                print(f"Error sending heartbeat: {e}")
            await asyncio.sleep(10)

    async def claim_and_execute_jobs(self):
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Queue)
                .where(Queue.is_paused == False)
            )
            queues = result.scalars().all()
            
            for queue in queues:
                await self.process_queue(db, queue)

    async def process_queue(self, db: AsyncSession, queue: Queue):
        result = await db.execute(
            select(Job)
            .where(
                Job.queue_id == queue.id,
                Job.status == "queued",
                (Job.scheduled_at == None) | (Job.scheduled_at <= datetime.utcnow())
            )
            .order_by(Job.priority.desc(), Job.created_at)
            .limit(queue.concurrency_limit)
        )
        jobs = result.scalars().all()
        
        for job in jobs:
            job.status = "claimed"
            job.started_at = datetime.utcnow()
            
            execution = JobExecution(
                job_id=job.id,
                worker_id=self.worker_id,
                started_at=datetime.utcnow(),
                status="running"
            )
            db.add(execution)
            await db.commit()
            
            await self.execute_job(db, job, execution)

    async def execute_job(self, db: AsyncSession, job: Job, execution: JobExecution):
        print(f"Executing job {job.id}...")
        try:
            await asyncio.sleep(1)
            execution.status = "completed"
            execution.completed_at = datetime.utcnow()
            execution.output = {"result": "success"}
            
            job.status = "completed"
            job.completed_at = datetime.utcnow()
        except Exception as e:
            execution.status = "failed"
            execution.completed_at = datetime.utcnow()
            execution.error_message = str(e)
            
            job.status = "failed"
            job.failed_at = datetime.utcnow()
        finally:
            await db.commit()

if __name__ == "__main__":
    worker = JobWorker()
    try:
        asyncio.run(worker.start())
    except KeyboardInterrupt:
        asyncio.run(worker.stop())
