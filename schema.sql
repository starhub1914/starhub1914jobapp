-- =============================================================================
-- Database Schema DDL for LinkedIn Job Application Bot
-- Compatible with PostgreSQL 15+ & Microsoft SQL Server 2019+
-- =============================================================================

-- Table: candidate_profile
-- Stores Ethan Cuevas's candidate profile details and fallback configurations
CREATE TABLE IF NOT EXISTS candidate_profile (
    candidate_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    notice_period VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    cv_filename VARCHAR(255) NOT NULL,
    github_url VARCHAR(255),
    linkedin_url VARCHAR(255),
    fallback_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: job_applications
-- Primary execution audit log tracking job evaluation and submission status
CREATE TABLE IF NOT EXISTS job_applications (
    job_id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(150) NOT NULL,
    date_posted TIMESTAMP NOT NULL,
    posting_age_days INT NOT NULL,
    easy_apply BOOLEAN NOT NULL DEFAULT TRUE,
    match_score DECIMAL(5, 2) DEFAULT 0.00,
    eval_status VARCHAR(50) NOT NULL, -- 'DISCOVERED', 'EVALUATED_PASS', 'EVALUATED_SKIP', 'APPLIED', 'FAILED', 'RETRY'
    skip_reason TEXT,
    cover_letter_text TEXT,
    screenshot_path VARCHAR(500),
    error_log TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_job_applications_status ON job_applications(eval_status);
CREATE INDEX idx_job_applications_score ON job_applications(match_score);
CREATE INDEX idx_job_applications_date ON job_applications(date_posted);

-- Table: screening_rules
-- Verified Q&A facts and dynamic screening question mapping
CREATE TABLE IF NOT EXISTS screening_rules (
    rule_id VARCHAR(50) PRIMARY KEY,
    keyword_pattern VARCHAR(255) NOT NULL,
    answer_type VARCHAR(50) NOT NULL, -- 'VERIFIED_FACT', 'NUMERIC', 'BOOLEAN', 'FALLBACK'
    answer_value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: retry_queue
-- Queue for handling transient errors and deferred DOM submission retries
CREATE TABLE IF NOT EXISTS retry_queue (
    queue_id SERIAL PRIMARY KEY,
    job_id VARCHAR(100) NOT NULL REFERENCES job_applications(job_id) ON DELETE CASCADE,
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    next_retry_at TIMESTAMP NOT NULL,
    last_error TEXT,
    status VARCHAR(50) DEFAULT 'PENDING', -- 'PENDING', 'PROCESSING', 'COMPLETED', 'EXHAUSTED'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_retry_queue_status_next ON retry_queue(status, next_retry_at);

-- Initial Seed Data: Ethan Cuevas Context Profile
INSERT INTO candidate_profile (
    candidate_id, full_name, email, phone, notice_period, location, cv_filename, github_url, linkedin_url, fallback_response
) VALUES (
    'ethan_cuevas',
    'Ethan Cuevas',
    'chael.cuevas@gmail.com',
    '8202 0452',
    'Immediate',
    'Singapore',
    'Ethan_Cuevas_Cuevas_CV_SG.pdf',
    'https://github.com/ethancuevas',
    'https://linkedin.com/in/ethancuevas',
    'No direct production experience, but proven ability to adopt new stacks rapidly (e.g., learned Laravel to production code in 14 days).'
) ON CONFLICT (candidate_id) DO NOTHING;

-- Initial Seed Data: Core Screening Fact Rules
INSERT INTO screening_rules (rule_id, keyword_pattern, answer_type, answer_value) VALUES
('sr_1', '(?i)years of.*python', 'NUMERIC', '5'),
('sr_2', '(?i)years of.*java', 'NUMERIC', '4'),
('sr_3', '(?i)notice period|availability', 'VERIFIED_FACT', 'Immediate'),
('sr_4', '(?i)singapore citizen|work authorization|located in singapore', 'BOOLEAN', 'Yes')
ON CONFLICT (rule_id) DO NOTHING;
