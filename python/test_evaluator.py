"""
Unit tests for Python 3.14 Async Engine and LLM Evaluator.
"""

import unittest
import asyncio
from python.config import CandidateProfile, SearchConfig
from python.evaluator import LLMEvaluator


class TestLLMEvaluator(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.candidate = CandidateProfile()
        self.config = SearchConfig()
        self.evaluator = LLMEvaluator(self.candidate, self.config)

    async def test_posting_age_filter(self):
        # Age > 7 days should be dropped automatically
        result = await self.evaluator.evaluate_job(
            job_id="test_01",
            job_title="Python Developer",
            company="Tech SG",
            posting_age_days=10,
            job_description="Python FastAPI backend developer"
        )
        self.assertFalse(result.pass_eval)
        self.assertIn("exceeds maximum threshold", result.skip_reason)

    async def test_high_relevance_job(self):
        # Highly relevant job description should pass evaluation
        result = await self.evaluator.evaluate_job(
            job_id="test_02",
            job_title="Senior Python & Java Developer",
            company="Central Techno Hub",
            posting_age_days=2,
            job_description="Seeking developer with Python, FastAPI, Java, Spring Boot, SQL Server, and IBM MQ experience."
        )
        self.assertTrue(result.pass_eval)
        self.assertGreaterEqual(result.match_score, 75.0)


if __name__ == "__main__":
    unittest.main()
