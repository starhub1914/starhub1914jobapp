# End-to-End Technical Specification & Architecture: LinkedIn Job Application Bot

## 1. System Overview & Executive Summary

The **LinkedIn Job Application Bot** is an enterprise-grade automated job discovery, relevance evaluation, and dynamic application submission system built using modern runtime specifications: **Python 3.14 (Async Engine with Playwright & FastAPI)** and **Java 26 (Virtual Threads Engine with HttpClient HTTP/3 & Playwright Java)**.

The system targets tech roles in Singapore for **Ethan Cuevas**, executing search queries, analyzing unstructured Job Descriptions against verified candidate qualifications using LLM evaluation models, and executing multi-step form applications using browser automation with anti-detection and dynamic fallback answer generation.

---

## 2. Target Candidate Profile & Qualifications Context

- **Candidate Name**: Ethan Cuevas
- **Current Location**: Singapore (Available immediately)
- **Contact Info**: `chael.cuevas@gmail.com` | `+65 8202 0452`
- **Notice Period**: Immediate
- **Primary Technical Stack**:
  - **Languages & Frameworks**: Python (FastAPI, Asyncio), Java (J2EE, Spring Boot), PHP (Laravel), JavaScript (Node.js/React), C# (.NET Core)
  - **Data & Middleware**: SQL Server, PostgreSQL, IBM MQ, ISO 20022 Messaging Standard
  - **Specializations**: Artificial Intelligence, Distributed Microservices, High-Throughput Financial Systems
- **Key Career Highlights**:
  - Founder @ **Central Techno Hub**
  - BSc in Computer Science with **AI Excellence Award**
  - Fast stack adoption: Demonstrated learning and shipping production-grade Laravel in 14 days.
- **CV Artifact**: `Ethan_Cuevas_Cuevas_CV_SG.pdf`
- **Missing Technology Fallback Response**:
  > *"No direct production experience, but proven ability to adopt new stacks rapidly (e.g., learned Laravel to production code in 14 days)."*

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
|   AI Engineer, Systems Analyst|                         | - HTTP/3 Async LLM Call       |
| - Filter: SG, Easy Apply      |                         |                               |
+---------------+---------------+                         +---------------+---------------+
                |                                                         |
                +---------------------------------+-----------------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                | MODULE 3 & 4: FORM FILL & BROWSER |
                                | - Multi-step Easy Apply dialog    |
                                | - Screening Q&A dynamic logic     |
                                | - Anti-detection human timing     |
                                | - Dynamic screenshot capture      |
                                +-----------------+-----------------+
                                                  |
                                                  v
                                +-----------------------------------+
                                | MODULE 5: AUDIT & STORAGE ENGINE  |
                                | - PostgreSQL / SQL Server Schema  |
                                | - Status: APPLIED, SKIPPED, FAILED|
                                | - Retry Queues & Trace Logging    |
                                +-----------------------------------+
```

---

## 4. Detailed Module Specifications

### Module 1: Job Search & Scraper Service
- **Search Parameters**:
  - **Keywords**: `"Software Engineer"`, `"Full Stack Developer"`, `"Python Developer"`, `"Backend Engineer"`, `"AI Engineer"`, `"Systems Analyst"`
  - **Location**: `Singapore` (Geo ID filter)
  - **Posting Age Constraint**: `f_TPR=r604800` (<= 7 days relative to runtime timestamp)
  - **Application Type**: `f_AL=true` (`Easy Apply` enabled)
- **Extraction Rules**:
  - Parse job element cards for `job_id`, `title`, `company`, `location`, `posted_date`, `job_url`, `description`.

### Module 2: LLM Relevance & Scoring Engine
- **Prompt Specification**:
  ```text
  System: You are an expert technical recruiter analyzing job postings for candidate Ethan Cuevas.
  Candidate Qualifications:
  - Stack: Python (FastAPI), Java (J2EE), PHP (Laravel), JavaScript, C#, SQL Server, IBM MQ, ISO 20022.
  - Education: BSc Computer Science (AI Excellence Award).
  - Background: Founder @ Central Techno Hub. Rapid stack learning capability.

  Job Description:
  {job_description}

  Instructions:
  1. Extract core required skills and qualifications.
  2. Calculate overall Match Score (0 - 100%).
  3. Determine pass/fail boolean (Match Score >= 75%).
  4. Return valid JSON:
  {
     "match_score": 85,
     "pass_eval": true,
     "required_skills": ["Python", "FastAPI", "PostgreSQL"],
     "missing_skills": ["Docker"],
     "reason": "Strong match with Python FastAPI experience."
  }
  ```
- **Enforcement Logic**: Drop candidate evaluation if `match_score < 75%` or `posting_age > 7 days`. Log detailed skip reasoning into storage.

### Module 3 & 4: Dynamic Form Processing & Browser Automation Engine
- **Form Solver Rules**:
  - Contact inputs: Email -> `chael.cuevas@gmail.com`, Phone -> `8202 0452`.
  - Notice Period -> `Immediate`.
  - Resume attachment -> `Ethan_Cuevas_Cuevas_CV_SG.pdf`.
  - Screening Questions:
    - If question matches candidate experience -> fill verified metric/fact (e.g. Years of Python experience -> `5`).
    - If question references unknown/unlisted technology -> fill standard fallback: *"No direct production experience, but proven ability to adopt new stacks rapidly (e.g., learned Laravel to production code in 14 days)."*
- **Anti-Detection Strategy**:
  - Humanized mouse jittering, random input delay (`50ms` - `200ms`), scroll behavior simulation.
  - Browser context configured with realistic user agents, timezone (`Asia/Singapore`), and WebGL vendor masking.
  - DOM Exception capture: Automatically saves screenshot to `./screenshots/{job_id}_error.png` on step failure.

### Module 5: Storage & Execution Audit Logging
- System maintains real-time records for every encountered job listing.
- Status values: `DISCOVERED`, `EVALUATED_PASS`, `EVALUATED_SKIP`, `APPLIED`, `FAILED`, `RETRY`.

---

## 5. Sequence Diagram: Job Discovery to Application

```
Candidate Bot        LinkedIn API / Web           LLM Evaluator           Database Log
     |                        |                         |                      |
     |---- Search Jobs ------>|                         |                      |
     |<--- Return Listings ---|                         |                      |
     |                        |                         |                      |
     |---- Check Age <=7d --->|                         |                      |
     |     (Drop if >7d)      |                         |                      |
     |                                                  |                      |
     |------------------- Evaluate JD ----------------->|                      |
     |<---------------- Score & JSON Response ----------|                      |
     |                                                  |                      |
     |---- If Score < 75% -> Log SKIPPED ------------------------------------->|
     |                                                                         |
     |---- If Score >= 75%: Launch Browser Dialog ---->|                       |
     |---- Step 1: Personal Info (Email/Phone)        |                       |
     |---- Step 2: Upload CV (Ethan_Cuevas...)        |                       |
     |---- Step 3: Screening Q&A (Verified/Fallback)  |                       |
     |---- Step 4: Submit Application                 |                       |
     |                                                                         |
     |------------------- Log APPLIED / FAILED ------------------------------->|
```
