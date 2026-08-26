package com.cth.model;

import java.time.LocalDateTime;

/**
 * JobApplication Entity Model for DB persistence and audit logging.
 */
public class JobApplication {

    private String jobId;
    private String title;
    private String company;
    private String location;
    private String linkedinUrl;
    private LocalDateTime datePosted;
    private int postingAgeDays;
    private boolean easyApply = true;
    private double matchScore;
    private String evalStatus;
    private String skipReason;
    private String coverLetterText;
    private String screenshotPath;
    private String errorLog;
    private LocalDateTime timestamp = LocalDateTime.now();

    public JobApplication() {}

    public JobApplication(String jobId, String title, String company, String location,
                          int postingAgeDays, double matchScore, String evalStatus, String skipReason) {
        this.jobId = jobId;
        this.title = title;
        this.company = company;
        this.location = location;
        this.linkedinUrl = "https://www.linkedin.com/jobs/view/" + jobId;
        this.datePosted = LocalDateTime.now().minusDays(postingAgeDays);
        this.postingAgeDays = postingAgeDays;
        this.matchScore = matchScore;
        this.evalStatus = evalStatus;
        this.skipReason = skipReason;
    }

    // Getters and Setters
    public String getJobId() { return jobId; }
    public void setJobId(String jobId) { this.jobId = jobId; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getCompany() { return company; }
    public void setCompany(String company) { this.company = company; }

    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }

    public String getLinkedinUrl() { return linkedinUrl; }
    public void setLinkedinUrl(String linkedinUrl) { this.linkedinUrl = linkedinUrl; }

    public LocalDateTime getDatePosted() { return datePosted; }
    public void setDatePosted(LocalDateTime datePosted) { this.datePosted = datePosted; }

    public int getPostingAgeDays() { return postingAgeDays; }
    public void setPostingAgeDays(int postingAgeDays) { this.postingAgeDays = postingAgeDays; }

    public boolean isEasyApply() { return easyApply; }
    public void setEasyApply(boolean easyApply) { this.easyApply = easyApply; }

    public double getMatchScore() { return matchScore; }
    public void setMatchScore(double matchScore) { this.matchScore = matchScore; }

    public String getEvalStatus() { return evalStatus; }
    public void setEvalStatus(String evalStatus) { this.evalStatus = evalStatus; }

    public String getSkipReason() { return skipReason; }
    public void setSkipReason(String skipReason) { this.skipReason = skipReason; }

    public String getCoverLetterText() { return coverLetterText; }
    public void setCoverLetterText(String coverLetterText) { this.coverLetterText = coverLetterText; }

    public String getScreenshotPath() { return screenshotPath; }
    public void setScreenshotPath(String screenshotPath) { this.screenshotPath = screenshotPath; }

    public String getErrorLog() { return errorLog; }
    public void setErrorLog(String errorLog) { this.errorLog = errorLog; }

    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
}
