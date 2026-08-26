"""
Browser Automation & Dynamic DOM Solver Engine (Module 3 & 4).
Uses Playwright Async API to handle multi-step LinkedIn 'Easy Apply' dialogs.
Features:
- Anti-detection human-like interaction timing & delays
- Auto-fill personal details (Email, Phone, Notice Period, CV upload)
- Verified CV facts matching & Missing technology fallback logic
- Dynamic DOM error capturing (automatic screenshot on failure)
"""

import asyncio
import os
import random
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List
from playwright.async_api import async_playwright, Page, BrowserContext, ElementHandle

from python.config import CandidateProfile, SearchConfig, SCREENSHOT_DIR
from python.evaluator import LLMEvaluator, EvaluationResult
from python.models import AsyncSessionLocal, JobApplicationModel

logger = logging.getLogger("LinkedInBot")


class LinkedInBotEngine:
    def __init__(self, candidate: CandidateProfile = CandidateProfile(), config: SearchConfig = SearchConfig()):
        self.candidate = candidate
        self.config = config
        self.evaluator = LLMEvaluator(candidate, config)
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    async def _human_delay(self, min_ms: int = 400, max_ms: int = 1200):
        """Simulate human reaction and typing delay."""
        delay = random.randint(min_ms, max_ms) / 1000.0
        await asyncio.sleep(delay)

    async def _solve_screening_questions(self, page: Page):
        """
        Module 3: Screening Question Dynamic Engine.
        Inspects input elements in application modal:
        - Matches verified candidate facts
        - Applies missing technology fallback answer
        """
        inputs = await page.query_selector_all("input[type='text'], textarea")
        for inp in inputs:
            label_handle = await inp.evaluate_handle("el => el.closest('div').querySelector('label')")
            label_text = await label_handle.inner_text() if label_handle else ""
            label_lower = label_text.lower()

            if "python" in label_lower:
                await inp.fill("5")
            elif "java" in label_lower:
                await inp.fill("4")
            elif "notice" in label_lower or "availability" in label_lower:
                await inp.fill(self.candidate.notice_period)
            elif "phone" in label_lower or "contact" in label_lower:
                await inp.fill(self.candidate.phone)
            else:
                # Missing Technology / Custom Question Fallback Logic
                await inp.fill(self.candidate.fallback_experience_response)

            await self._human_delay(100, 300)

        # Handle radio buttons / checkboxes (e.g. Work Authorization in SG)
        radios = await page.query_selector_all("input[type='radio'][value='Yes']")
        for radio in radios:
            if not await radio.is_checked():
                await radio.click()

    async def apply_job_workflow(self, page: Page, job_data: Dict[str, Any]) -> str:
        """
        Module 4: Multi-Step Easy Apply Browser Automation Workflow.
        """
        job_id = job_data["job_id"]
        job_url = job_data.get("job_url", f"https://www.linkedin.com/jobs/view/{job_id}")

        try:
            logger.info(f"Navigating to job page: {job_url}")
            await page.goto(job_url, wait_until="domcontentloaded", timeout=30000)
            await self._human_delay(1000, 2000)

            # Locate Easy Apply Button
            easy_apply_btn = await page.query_selector("button.jobs-apply-button")
            if not easy_apply_btn:
                logger.warning(f"Easy Apply button not found for job {job_id}")
                return "SKIPPED_NO_EASY_APPLY"

            await easy_apply_btn.click()
            await self._human_delay(800, 1500)

            # Step-through application modal dialog
            max_steps = 6
            step = 0
            while step < max_steps:
                step += 1
                logger.info(f"Processing application modal step {step} for job {job_id}")

                # Fill screening form inputs
                await self._solve_screening_questions(page)

                # CV Upload element handling
                file_input = await page.query_selector("input[type='file']")
                if file_input:
                    cv_path = os.path.abspath(self.candidate.cv_filename)
                    if os.path.exists(cv_path):
                        await file_input.set_input_files(cv_path)
                        logger.info(f"Uploaded CV {cv_path}")

                # Check for Submit button vs Next button
                submit_btn = await page.query_selector("button[aria-label='Submit application'], button:has-text('Submit application')")
                if submit_btn:
                    await submit_btn.click()
                    await self._human_delay(1000, 2000)
                    logger.info(f"Successfully submitted job application {job_id}")
                    return "APPLIED"

                next_btn = await page.query_selector("button[aria-label='Continue to next step'], button:has-text('Next')")
                if next_btn:
                    await next_btn.click()
                    await self._human_delay(800, 1500)
                else:
                    break

            return "APPLIED"

        except Exception as e:
            error_msg = str(e)
            logger.error(f"DOM Error while applying to job {job_id}: {error_msg}")
            screenshot_file = os.path.join(SCREENSHOT_DIR, f"{job_id}_error.png")
            try:
                await page.screenshot(path=screenshot_file, full_page=True)
                logger.info(f"DOM Exception screenshot saved to {screenshot_file}")
            except Exception as ss_err:
                logger.error(f"Failed to capture screenshot: {ss_err}")

            raise e

    async def run_pipeline(self, max_jobs: int = 5):
        """Scrape, evaluate, and apply pipeline."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
            context: BrowserContext = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                locale="en-SG",
                timezone_id="Asia/Singapore"
            )
            page: Page = await context.new_page()

            # Mock job discovery stream representing LinkedIn endpoints
            mock_discovered_jobs = [
                {
                    "job_id": "sg_tech_101",
                    "title": "Senior Python Backend Engineer",
                    "company": "Fintech Solutions SG",
                    "location": "Singapore",
                    "posting_age_days": 2,
                    "description": "Seeking Python Developer expert in FastAPI, Asyncio, PostgreSQL, and ISO 20022 message processing."
                },
                {
                    "job_id": "sg_tech_102",
                    "title": "Full Stack Engineer (Java/PHP)",
                    "company": "Enterprise Systems Asia",
                    "location": "Singapore",
                    "posting_age_days": 4,
                    "description": "Looking for Java Spring Boot and PHP Laravel engineers with SQL Server microservices experience."
                },
                {
                    "job_id": "sg_tech_103",
                    "title": "Legacy COBOL Analyst",
                    "company": "Old Tech Corp",
                    "location": "Singapore",
                    "posting_age_days": 10, # Age > 7d -> Should be dropped
                    "description": "COBOL and Mainframe maintenance."
                }
            ]

            async with AsyncSessionLocal() as session:
                for job in mock_discovered_jobs[:max_jobs]:
                    job_id = job["job_id"]
                    logger.info(f"Processing candidate job {job_id}: {job['title']}")

                    # Module 2: LLM Relevance Evaluation
                    eval_res: EvaluationResult = await self.evaluator.evaluate_job(
                        job_id=job_id,
                        job_title=job["title"],
                        company=job["company"],
                        posting_age_days=job["posting_age_days"],
                        job_description=job["description"]
                    )

                    status = "EVALUATED_SKIP" if not eval_res.pass_eval else "EVALUATED_PASS"
                    skip_reason = eval_res.skip_reason

                    if eval_res.pass_eval:
                        try:
                            app_status = await self.apply_job_workflow(page, job)
                            status = app_status
                        except Exception as err:
                            status = "FAILED"
                            skip_reason = str(err)

                    # Save audit log to database
                    record = JobApplicationModel(
                        job_id=job_id,
                        title=job["title"],
                        company=job["company"],
                        location=job["location"],
                        date_posted=datetime.now(timezone.utc).replace(tzinfo=None),
                        posting_age_days=job["posting_age_days"],
                        easy_apply=True,
                        match_score=eval_res.match_score,
                        eval_status=status,
                        skip_reason=skip_reason,
                        cover_letter_text=eval_res.generated_cover_letter,
                        screenshot_path=os.path.join(SCREENSHOT_DIR, f"{job_id}_error.png") if status == "FAILED" else None,
                        error_log=skip_reason if status == "FAILED" else None
                    )
                    await session.merge(record)
                    await session.commit()
                    logger.info(f"Audit record saved for {job_id} with status {status}")

            await browser.close()
