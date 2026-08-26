# End-to-End Technical Specification & Architecture: LinkedIn Job Application Bot

## 1. System Overview & Executive Summary

The **LinkedIn Job Application Bot** is an enterprise-grade automated job discovery, relevance evaluation, and dynamic application submission system built using modern runtime specifications: **Python 3.14 (Async Engine with Playwright & FastAPI)** and **Java 26 (Virtual Threads Engine with HttpClient HTTP/3 & Playwright Java)** under the **`com.cth`** (Central Techno Hub) package structure.

### Dynamic Environment Variable Configuration & Dashboard Endpoints
All candidate personal details, search filters, and execution parameters are **fully configurable via system environment variables**. When no environment variables are explicitly passed, the system defaults to Ethan Cuevas's profile.

The system features dashboard reporting endpoints in both Python FastAPI (`/applications`) and Java 26 CLI/Service summary modes, listing all applied jobs, company names, application timestamps, evaluation match scores, and direct LinkedIn job URL links (`https://www.linkedin.com/jobs/view/{job_id}`).

---

## 2. Configurable Candidate Profile & Environment Variables

The application reads candidate profile information directly from runtime environment variables:

| Environment Variable | Description | Default Value |
| :--- | :--- | :--- |
| `CANDIDATE_NAME` | Candidate Full Name | `Ethan Cuevas` |
| `CANDIDATE_EMAIL` | Application Contact Email | `chael.cuevas@gmail.com` |
| `CANDIDATE_PHONE` | Application Contact Phone | `8202 0452` |
| `CANDIDATE_LOCATION` | Primary Candidate Location | `Singapore` |
| `CANDIDATE_NOTICE_PERIOD` | Notice Period Availability | `Immediate` |
| `CANDIDATE_CV_FILENAME` | Path to Resume PDF file | `Ethan_Cuevas_Cuevas_CV_SG.pdf` |
| `CANDIDATE_GITHUB_URL` | GitHub Profile Link | `https://github.com/ethancuevas` |
| `CANDIDATE_LINKEDIN_URL` | LinkedIn Profile Link | `https://linkedin.com/in/ethancuevas` |
| `CANDIDATE_FALLBACK_RESPONSE` | Screening Q&A Fallback Answer | *"No direct production experience, but proven ability to adopt new stacks rapidly (e.g., learned Laravel to production code in 14 days)."* |
| `MIN_MATCH_SCORE` | Minimum Match Score Filter (%) | `75.0` |
| `MAX_POSTING_AGE_DAYS` | Max Job Posting Age Filter (Days) | `7` |

---

## 3. High-Level Architecture & Component Diagram

```
+-----------------------------------------------------------------------------------+
|                                  ORCHESTRATOR LAYER                               |
|   +----------------------------------+     +----------------------------------+   |
|   |  Python 3.14 Engine (FastAPI)   |     |   Java 26 Virtual Threads Engine |   |
|   +----------------------------------+     +----------------------------------+   |
+-----------------------------------------+-----------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                                                   |
        v                                                                   v
+-------------------------------+                         +-------------------------------+
|  MODULE 1: SEARCH & SCRAPER   |                         |   MODULE 2: LLM EVALUATOR     |
| - LinkedIn Endpoint Search    |                         | - Skills Extraction           |
| - Terms: Software Engineer,   |                         | - Match Score (0-100%)        |
|   Full Stack, Python, Backend |                         | - Filter: Age <=7d & Score>=75|
|   AI Engineer, Systems Analyst|                         | - Configurable Env Parameters |
| - Filter: SG, Easy Apply      |                         |                               |
+---------------+---------------+                         +---------------+---------------+
                |                                                         |
                +---------------------------------+-----------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                | MODULE 3 & 4: FORM FILL & BROWSER |
                                | - Multi-step Easy Apply dialog    |
                                | - Configurable Screening Q&A      |
                                | - Anti-detection human timing     |
                                | - Dynamic screenshot capture      |
                                +-----------------+-----------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                | MODULE 5: AUDIT & DASHBOARD LAYER |
                                | - PostgreSQL / SQL Server Schema  |
                                | - Status: APPLIED, SKIPPED, FAILED|
                                | - Applied Jobs & Direct Links View|
                                +-----------------------------------+
```

---

## 4. Dashboard Endpoint Specifications

### Applied Jobs Listing Endpoint (`GET /applications`)
- **JSON Response Schema**:
```json
[
  {
    "job_id": "sg_tech_101",
    "title": "Senior Python Backend Engineer",
    "company": "Fintech Solutions SG",
    "location": "Singapore",
    "linkedin_url": "https://www.linkedin.com/jobs/view/sg_tech_101",
    "posting_age_days": 2,
    "match_score": 85.0,
    "eval_status": "APPLIED",
    "skip_reason": null,
    "applied_at": "2026-02-26T04:50:00.000000"
  }
]
```

---

## 5. Detailed Module Specifications

### Module 1: Job Search & Scraper Service
- **Search Parameters**:
  - **Keywords**: `"Software Engineer"`, `"Full Stack Developer"`, `"Python Developer"`, `"Backend Engineer"`, `"AI Engineer"`, `"Systems Analyst"`
  - **Location**: `Singapore` (Geo ID filter, configurable via `CANDIDATE_LOCATION`)
  - **Posting Age Constraint**: `f_TPR=r604800` (<= 7 days relative to runtime timestamp, configurable via `MAX_POSTING_AGE_DAYS`)
  - **Application Type**: `f_AL=true` (`Easy Apply` enabled)

### Module 2: LLM Relevance & Scoring Engine (Zero-License Enabled)
- Standalone zero-cost heuristic evaluator fallback ensures candidate relevance calculation is computed locally without external paid cloud calls.

### Module 3 & 4: Dynamic Form Processing & Browser Automation Engine
- **Form Solver Rules**:
  - Contact inputs read directly from environment variables: Email -> `CANDIDATE_EMAIL`, Phone -> `CANDIDATE_PHONE`.
  - Notice Period -> `CANDIDATE_NOTICE_PERIOD`.
  - Resume attachment -> `CANDIDATE_CV_FILENAME`.
  - Screening Questions Fallback -> `CANDIDATE_FALLBACK_RESPONSE`.

### Module 5: Storage & Execution Audit Logging
- System maintains real-time records for every encountered job listing.
- Status values: `DISCOVERED`, `EVALUATED_PASS`, `EVALUATED_SKIP`, `APPLIED`, `FAILED`, `RETRY`.
