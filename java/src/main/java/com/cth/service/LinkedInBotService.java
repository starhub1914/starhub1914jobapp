package com.cth.service;

import com.cth.model.JobApplication;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Java 26 Virtual Threads Execution Engine (Module 1, 3, 4, 5).
 * Leverages Java 26 `Executors.newVirtualThreadPerTaskExecutor()` for high-concurrency job processing.
 */
public class LinkedInBotService {

    private final LLMEvaluatorService llmEvaluator;

    public LinkedInBotService(LLMEvaluatorService llmEvaluator) {
        this.llmEvaluator = llmEvaluator;
    }

    /**
     * Executes concurrent job processing pipelines using Java 26 Virtual Threads.
     */
    public void runConcurrentPipeline(List<JobRecord> jobs) {
        // Java 26 Virtual Thread Per Task Executor
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<?>> futures = new ArrayList<>();
            for (JobRecord job : jobs) {
                futures.add(executor.submit(() -> processJobTask(job)));
            }

            for (Future<?> f : futures) {
                f.get(); // Wait for virtual thread task completions
            }
        } catch (Exception e) {
            System.err.println("Error during virtual threads pipeline execution: " + e.getMessage());
        }
    }

    private void processJobTask(JobRecord job) {
        long threadId = Thread.currentThread().threadId();
        System.out.println("[VirtualThread-" + threadId + "] Processing Job " + job.jobId() + ": " + job.title());

        // Step 1: LLM Relevance Evaluation & Posting Age Filter (<= 7 days)
        LLMEvaluatorService.EvaluationResult eval = llmEvaluator.evaluateJob(
                job.jobId(), job.title(), job.company(), job.postingAgeDays(), job.description()
        );

        JobApplication appRecord = new JobApplication(
                job.jobId(), job.title(), job.company(), "Singapore",
                job.postingAgeDays(), eval.matchScore(),
                eval.passEval() ? "EVALUATED_PASS" : "EVALUATED_SKIP",
                eval.skipReason()
        );

        if (!eval.passEval()) {
            System.out.println("[VirtualThread-" + threadId + "] Skipped job " + job.jobId() + ": " + eval.skipReason());
            return;
        }

        // Step 2: Playwright / Browser Automation Step-through
        try {
            System.out.println("[VirtualThread-" + threadId + "] Launching Playwright DOM step-through for job " + job.jobId());
            Thread.sleep(200); // Anti-detection human interaction timing simulation

            // Candidate form inputs auto-fill simulation for Ethan Cuevas
            String candidateEmail = "chael.cuevas@gmail.com";
            String candidatePhone = "8202 0452";
            String fallbackAnswer = "No direct production experience, but proven ability to adopt new stacks rapidly (e.g., learned Laravel to production code in 14 days).";

            appRecord.setEvalStatus("APPLIED");
            System.out.println("[VirtualThread-" + threadId + "] Successfully applied to job " + job.jobId() + " (Email: " + candidateEmail + ")");

        } catch (Exception domEx) {
            System.err.println("DOM Exception for " + job.jobId() + ": " + domEx.getMessage());
            appRecord.setEvalStatus("FAILED");
            appRecord.setErrorLog(domEx.getMessage());
            appRecord.setScreenshotPath("./screenshots/" + job.jobId() + "_java_error.png");
        }
    }

    public record JobRecord(String jobId, String title, String company, int postingAgeDays, String description) {}
}
