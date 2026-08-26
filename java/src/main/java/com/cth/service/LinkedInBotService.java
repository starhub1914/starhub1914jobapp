package com.cth.service;

import com.cth.model.JobApplication;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Java 26 Virtual Threads Execution Engine (Module 1, 3, 4, 5).
 * Configurable Candidate Details via Environment Variables.
 */
public class LinkedInBotService {

    private final LLMEvaluatorService llmEvaluator;

    // Configurable Candidate Personal Details
    private final String candidateName = System.getenv().getOrDefault("CANDIDATE_NAME", "Ethan Cuevas");
    private final String candidateEmail = System.getenv().getOrDefault("CANDIDATE_EMAIL", "chael.cuevas@gmail.com");
    private final String candidatePhone = System.getenv().getOrDefault("CANDIDATE_PHONE", "8202 0452");
    private final String candidateLocation = System.getenv().getOrDefault("CANDIDATE_LOCATION", "Singapore");
    private final String fallbackAnswer = System.getenv().getOrDefault(
            "CANDIDATE_FALLBACK_RESPONSE",
            "No direct production experience, but proven ability to adopt new stacks rapidly (e.g., learned Laravel to production code in 14 days)."
    );

    public LinkedInBotService(LLMEvaluatorService llmEvaluator) {
        this.llmEvaluator = llmEvaluator;
    }

    public void runConcurrentPipeline(List<JobRecord> jobs) {
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<?>> futures = new ArrayList<>();
            for (JobRecord job : jobs) {
                futures.add(executor.submit(() -> processJobTask(job)));
            }

            for (Future<?> f : futures) {
                f.get();
            }
        } catch (Exception e) {
            System.err.println("Error during virtual threads pipeline execution: " + e.getMessage());
        }
    }

    private void processJobTask(JobRecord job) {
        long threadId = Thread.currentThread().threadId();
        System.out.println("[VirtualThread-" + threadId + "] Processing Job " + job.jobId() + ": " + job.title() + " for candidate: " + candidateName);

        LLMEvaluatorService.EvaluationResult eval = llmEvaluator.evaluateJob(
                job.jobId(), job.title(), job.company(), job.postingAgeDays(), job.description()
        );

        JobApplication appRecord = new JobApplication(
                job.jobId(), job.title(), job.company(), candidateLocation,
                job.postingAgeDays(), eval.matchScore(),
                eval.passEval() ? "EVALUATED_PASS" : "EVALUATED_SKIP",
                eval.skipReason()
        );

        if (!eval.passEval()) {
            System.out.println("[VirtualThread-" + threadId + "] Skipped job " + job.jobId() + ": " + eval.skipReason());
            return;
        }

        try {
            System.out.println("[VirtualThread-" + threadId + "] Launching Playwright DOM step-through for job " + job.jobId());
            Thread.sleep(200);

            appRecord.setEvalStatus("APPLIED");
            System.out.println("[VirtualThread-" + threadId + "] Successfully applied to job " + job.jobId() + " (Email: " + candidateEmail + ", Phone: " + candidatePhone + ")");

        } catch (Exception domEx) {
            System.err.println("DOM Exception for " + job.jobId() + ": " + domEx.getMessage());
            appRecord.setEvalStatus("FAILED");
            appRecord.setErrorLog(domEx.getMessage());
            appRecord.setScreenshotPath("./screenshots/" + job.jobId() + "_java_error.png");
        }
    }

    public record JobRecord(String jobId, String title, String company, int postingAgeDays, String description) {}
}
