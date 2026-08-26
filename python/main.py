"""
FastAPI Microservice Dashboard & Orchestrator CLI (Python 3.14).
"""

import asyncio
import sys
from contextlib import asynccontextmanager
from typing import List, Dict, Any

from python.models import init_db, AsyncSessionLocal, JobApplicationModel
from python.bot import LinkedInBotEngine

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
        title="Ethan Cuevas - LinkedIn Application Bot API",
        version="1.0.0",
        lifespan=lifespan
    )

    class JobApplicationResponse(BaseModel):
        job_id: str
        title: str
        company: str
        location: str
        posting_age_days: int
        match_score: float
        eval_status: str
        skip_reason: str | None

    @app.get("/health")
    async def health_check():
        return {
            "status": "online",
            "engine": "Python 3.14 Async Free-Threading",
            "candidate": bot.candidate.name,
            "target_location": bot.config.location
        }

    @app.post("/trigger-pipeline")
    async def trigger_pipeline(background_tasks: BackgroundTasks, max_jobs: int = 5):
        background_tasks.add_task(bot.run_pipeline, max_jobs)
        return {"message": f"Pipeline execution triggered for up to {max_jobs} jobs in background."}


async def run_cli():
    print("=========================================================================")
    print("Initializing Database & Executing Python 3.14 Job Application Bot Pipeline")
    print("Candidate: Ethan Cuevas | Location: Singapore")
    print("=========================================================================")
    await init_db()
    await bot.run_pipeline(max_jobs=5)
    print("=========================================================================")
    print("Python 3.14 Pipeline Execution Completed Successfully.")
    print("=========================================================================")


if __name__ == "__main__":
    asyncio.run(run_cli())
