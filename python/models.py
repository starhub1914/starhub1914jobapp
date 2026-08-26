"""
SQLAlchemy 2.0 Async Models and Database Configuration for Job Application Bot.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Float, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from python.config import DATABASE_URL


class Base(DeclarativeBase):
    pass


class JobApplicationModel(Base):
    __tablename__ = "job_applications"

    job_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(150), nullable=False)
    date_posted: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    posting_age_days: Mapped[int] = mapped_column(Integer, nullable=False)
    easy_apply: Mapped[bool] = mapped_column(Boolean, default=True)
    match_score: Mapped[float] = mapped_column(Float, default=0.0)
    eval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="DISCOVERED")
    skip_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cover_letter_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    screenshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
