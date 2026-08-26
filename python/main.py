"""
FastAPI Microservice Dashboard & Orchestrator CLI (Python 3.14).
Provides listing endpoint for all applied jobs, timestamps, company names, and LinkedIn URLs.
"""

import asyncio
import sys
from contextlib import asynccontextmanager
from typing import List, Dict, Any

from python.models import init_db, AsyncSessionLocal, JobApplicationModel
from python.bot import LinkedInBotEngine
from python.config import APP_NAME

try:
    from fastapi import FastAPI, BackgroundTasks, HTTPException
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    BaseModel = object

bot = LinkedInBotEngine()

if FASTAPI_AVAILABLE:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_db()
        yield

    app = FastAPI(
        title=APP_NAME,
        version="1.0.0",
        lifespan=lifespan
    )

    class JobApplicationResponse(BaseModel):
        job_id: str
        title: str
        company: str
        location: str
        linkedin_url: str
        posting_age_days: int
        match_score: float
        eval_status: str
        skip_reason: str | None
        applied_at: str

    @app.get("/health")
    async def health_check():
        return {
            "application_name": APP_NAME,
            "status": "online",
            "engine": "Python 3.14 Async Free-Threading",
            "candidate": bot.candidate.name,
            "target_location": bot.config.location
        }

    @app.post("/trigger-pipeline")
    async def trigger_pipeline(background_tasks: BackgroundTasks, max_jobs: int = 5):
        background_tasks.add_task(bot.run_pipeline, max_jobs)
        return {"message": f"Pipeline execution triggered for up to {max_jobs} jobs in background."}

    @app.get("/applications", response_model=List[JobApplicationResponse])
    async def list_applications():
        from sqlalchemy import select
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(JobApplicationModel))
            records = result.scalars().all()
            return [
                JobApplicationResponse(
                    job_id=r.job_id,
                    title=r.title,
                    company=r.company,
                    location=r.location,
                    linkedin_url=f"https://www.linkedin.com/jobs/view/{r.job_id}",
                    posting_age_days=r.posting_age_days,
                    match_score=r.match_score,
                    eval_status=r.eval_status,
                    skip_reason=r.skip_reason,
                    applied_at=r.timestamp.isoformat() if r.timestamp else ""
                ) for r in records
            ]


async def run_cli():
    print("=========================================================================")
    print(f"Initializing Database & Executing {APP_NAME} Pipeline")
    print(f"Candidate: {bot.candidate.name} | Location: {bot.config.location}")
    print("=========================================================================")
    await init_db()
    await bot.run_pipeline(max_jobs=5)
    print("=========================================================================")
    print("Python 3.14 Pipeline Execution Completed Successfully.")
    print("=========================================================================")


if __name__ == "__main__":
    asyncio.run(run_cli())
