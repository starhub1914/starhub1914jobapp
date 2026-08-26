"""
LLM Relevance & Scoring Engine (Module 2).
Uses Python 3.14 async HTTP calls to parse Job Descriptions, extract required skills,
and calculate Match Score (0-100%) against Ethan Cuevas's qualifications.
Enforces >= 75% match score & age <= 7 days filter.
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any
import urllib.request
import urllib.parse
from python.config import CandidateProfile, SearchConfig, LLM_API_KEY, LLM_ENDPOINT

logger = logging.getLogger("LLMEvaluator")


@dataclass
class EvaluationResult:
    job_id: str
    match_score: float
    pass_eval: bool
    skip_reason: str
    required_skills: List[str]
    missing_skills: List[str]
    generated_cover_letter: str


class LLMEvaluator:
    def __init__(self, candidate: CandidateProfile = CandidateProfile(), config: SearchConfig = SearchConfig()):
        self.candidate = candidate
        self.config = config

    def build_prompt(self, job_title: str, company: str, job_description: str) -> str:
        skills_str = ", ".join(self.candidate.core_skills)
        highlights_str = "; ".join(self.candidate.highlights)
        return f"""
System: You are a Lead Software Engineering Recruiter evaluating job descriptions for candidate Ethan Cuevas.

Candidate Background:
- Name: {self.candidate.name}
- Core Skills: {skills_str}
- Highlights: {highlights_str}
- Available: {self.candidate.notice_period} in {self.candidate.location}

Job Details:
- Title: {job_title}
- Company: {company}
- Job Description:
{job_description}

Instructions:
1. Extract key required skills from the job description.
2. Identify which required skills match Ethan's skills, and which are missing.
3. Calculate an overall Match Score from 0 to 100%.
4. Determine pass_eval (True if Match Score >= {self.config.min_match_score}, else False).
5. If pass_eval is False, provide a concise skip_reason.
6. Return ONLY a raw JSON object matching this schema:
{{
   "match_score": 85.0,
   "pass_eval": true,
   "required_skills": ["Python", "FastAPI"],
   "missing_skills": ["Docker"],
   "skip_reason": "",
   "cover_letter_text": "Dear Hiring Team..."
}}
"""

    def _sync_llm_call(self, prompt: str) -> str:
        payload = json.dumps({
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }).encode('utf-8')

        req = urllib.request.Request(
            LLM_ENDPOINT,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LLM_API_KEY}"
            }
        )
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode('utf-8'))
            return resp_data["choices"][0]["message"]["content"].strip()

    async def evaluate_job(
        self, job_id: str, job_title: str, company: str, posting_age_days: int, job_description: str
    ) -> EvaluationResult:
        # Enforce Posting Age Constraint strictly
        if posting_age_days > self.config.max_posting_age_days:
            reason = f"Job posting age ({posting_age_days} days) exceeds maximum threshold ({self.config.max_posting_age_days} days)."
            logger.info(f"Job {job_id} skipped: {reason}")
            return EvaluationResult(
                job_id=job_id,
                match_score=0.0,
                pass_eval=False,
                skip_reason=reason,
                required_skills=[],
                missing_skills=[],
                generated_cover_letter=""
            )

        prompt = self.build_prompt(job_title, company, job_description)

        # Calculate heuristic match score as fallback if LLM endpoint is mock/unavailable
        parsed_eval = self._fallback_heuristic_eval(job_description)

        # If real API key is configured, perform non-blocking LLM call via to_thread
        if LLM_API_KEY != "mock-key":
            try:
                content = await asyncio.to_thread(self._sync_llm_call, prompt)
                parsed = json.loads(content)
                parsed_eval.update(parsed)
            except Exception as e:
                logger.warning(f"LLM API call failed: {e}. Falling back to heuristic rule engine.")

        score = float(parsed_eval.get("match_score", 0.0))
        pass_eval = score >= self.config.min_match_score

        skip_reason = ""
        if not pass_eval:
            skip_reason = parsed_eval.get(
                "skip_reason",
                f"Match score {score}% is below threshold {self.config.min_match_score}%."
            )

        return EvaluationResult(
            job_id=job_id,
            match_score=score,
            pass_eval=pass_eval,
            skip_reason=skip_reason,
            required_skills=parsed_eval.get("required_skills", []),
            missing_skills=parsed_eval.get("missing_skills", []),
            generated_cover_letter=parsed_eval.get("cover_letter_text", f"Application for {job_title} at {company}")
        )

    def _fallback_heuristic_eval(self, description: str) -> Dict[str, Any]:
        desc_lower = description.lower()
        matched = [s for s in self.candidate.core_skills if s.lower() in desc_lower]
        score = min(100.0, max(50.0, len(matched) * 15.0 + 30.0))
        return {
            "match_score": score,
            "pass_eval": score >= self.config.min_match_score,
            "required_skills": matched,
            "missing_skills": [],
            "skip_reason": "" if score >= self.config.min_match_score else f"Heuristic score ({score}%) under threshold.",
            "cover_letter_text": f"Enthusiastic candidate Ethan Cuevas bringing skills in {', '.join(matched[:3])}."
        }
