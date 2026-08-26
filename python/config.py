"""
Configuration parameters for LinkedIn Job Application Bot.
Supports fully configurable candidate personal details & application metadata via Environment Variables.
Python 3.14 Async Engine target settings.
"""

import os
from dataclasses import dataclass, field
from typing import List

# Configurable Application Name (Default: "Software Development Document Environment" / "My Job App")
APP_NAME = os.getenv("APP_NAME", "Software Development Document Environment")


@dataclass
class CandidateProfile:
    name: str = field(default_factory=lambda: os.getenv("CANDIDATE_NAME", "Ethan Cuevas"))
    email: str = field(default_factory=lambda: os.getenv("CANDIDATE_EMAIL", "chael.cuevas@gmail.com"))
    phone: str = field(default_factory=lambda: os.getenv("CANDIDATE_PHONE", "8202 0452"))
    location: str = field(default_factory=lambda: os.getenv("CANDIDATE_LOCATION", "Singapore"))
    notice_period: str = field(default_factory=lambda: os.getenv("CANDIDATE_NOTICE_PERIOD", "Immediate"))
    cv_filename: str = field(default_factory=lambda: os.getenv("CANDIDATE_CV_FILENAME", "Ethan_Cuevas_Cuevas_CV_SG.pdf"))
    github_url: str = field(default_factory=lambda: os.getenv("CANDIDATE_GITHUB_URL", "https://github.com/ethancuevas"))
    linkedin_url: str = field(default_factory=lambda: os.getenv("CANDIDATE_LINKEDIN_URL", "https://linkedin.com/in/ethancuevas"))
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
    fallback_experience_response: str = field(default_factory=lambda: os.getenv(
        "CANDIDATE_FALLBACK_RESPONSE",
        "No direct production experience, but proven ability to adopt new stacks rapidly (e.g., learned Laravel to production code in 14 days)."
    ))


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
    location: str = field(default_factory=lambda: os.getenv("SEARCH_LOCATION", "Singapore"))
    max_posting_age_days: int = int(os.getenv("MAX_POSTING_AGE_DAYS", "7"))
    easy_apply_only: bool = os.getenv("EASY_APPLY_ONLY", "True").lower() == "true"
    min_match_score: float = float(os.getenv("MIN_MATCH_SCORE", "75.0"))


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./job_bot.db")
LLM_API_KEY = os.getenv("LLM_API_KEY", "mock-key")
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "https://api.openai.com/v1/chat/completions")
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "./screenshots")
