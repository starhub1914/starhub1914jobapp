"""
Configuration parameters for Ethan Cuevas's LinkedIn Job Application Bot.
Python 3.14 Async Engine target settings.
"""

import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class CandidateProfile:
    name: str = "Ethan Cuevas"
    email: str = "chael.cuevas@gmail.com"
    phone: str = "8202 0452"
    location: str = "Singapore"
    notice_period: str = "Immediate"
    cv_filename: str = "Ethan_Cuevas_Cuevas_CV_SG.pdf"
    github_url: str = "https://github.com/ethancuevas"
    linkedin_url: str = "https://linkedin.com/in/ethancuevas"
    core_skills: List[str] = field(default_factory=lambda: [
        "Python", "FastAPI", "Asyncio", "Java", "J2EE", "Spring Boot",
        "PHP", "Laravel", "JavaScript", "React", "C#", ".NET",
        "SQL Server", "PostgreSQL", "IBM MQ", "ISO 20022", "Artificial Intelligence"
    ])
    highlights: List[str] = field(default_factory=lambda: [
        "Founder @ Central Techno Hub",
        "BSc Computer Science with AI Excellence Award",
        "Fast stack adoption (learned Laravel to production code in 14 days)"
    ])
    fallback_experience_response: str = (
        "No direct production experience, but proven ability to adopt new stacks rapidly "
        "(e.g., learned Laravel to production code in 14 days)."
    )


@dataclass
class SearchConfig:
    keywords: List[str] = field(default_factory=lambda: [
        "Software Engineer",
        "Full Stack Developer",
        "Python Developer",
        "Backend Engineer",
        "AI Engineer",
        "Systems Analyst"
    ])
    location: str = "Singapore"
    max_posting_age_days: int = 7
    easy_apply_only: bool = True
    min_match_score: float = 75.0


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./job_bot.db")
LLM_API_KEY = os.getenv("LLM_API_KEY", "mock-key")
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "https://api.openai.com/v1/chat/completions")
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "./screenshots")
