package com.cth;

import com.cth.model.JobApplication;
import com.cth.service.LLMEvaluatorService;
import com.cth.service.LinkedInBotService;

import java.util.List;

/**
 * Main application entry point for Java 26 Virtual Threads Job Application Engine.
 * Package refactored to com.cth (Central Techno Hub).
 */
public class Application {

    public static void main(String[] args) {
        System.out.println("=========================================================================");
        System.out.println("Starting Java 26 Virtual Threads LinkedIn Job Application Engine (com.cth)");
        System.out.println("Candidate: Ethan Cuevas | Target Location: Singapore");
        System.out.println("=========================================================================");

        LLMEvaluatorService llmEvaluator = new LLMEvaluatorService();
        LinkedInBotService botService = new LinkedInBotService(llmEvaluator);

        List<LinkedInBotService.JobRecord> mockJobs = List.of(
                new LinkedInBotService.JobRecord(
                        "sg_java_201", "Lead Java Architect", "Fintech Bank SG", 1,
                        "Requires Java 26, Virtual Threads, Spring Boot microservices, ISO 20022 and IBM MQ."
                ),
                new LinkedInBotService.JobRecord(
                        "sg_java_202", "Python FastAPI Developer", "AI Central Hub", 3,
                        "Seeking Python developer proficient in FastAPI, Asyncio, SQL Server."
                ),
                new LinkedInBotService.JobRecord(
                        "sg_java_203", "Stale COBOL Engineer", "Old Tech Ltd", 12, // Age > 7d -> Skipped
                        "COBOL engineer needed."
                )
        );

        botService.runConcurrentPipeline(mockJobs);

        System.out.println("=========================================================================");
        System.out.println("Applied Jobs Summary (Java 26 Dashboard View):");
        System.out.println("-------------------------------------------------------------------------");
        for (JobApplication app : botService.getAllApplications()) {
            System.out.printf("• [%s] %s at %s | Match: %.1f%% | Date: %s | URL: %s%n",
                    app.getEvalStatus(), app.getTitle(), app.getCompany(),
                    app.getMatchScore(), app.getTimestamp(), app.getLinkedinUrl());
        }
        System.out.println("=========================================================================");
        System.out.println("Java 26 Virtual Threads Pipeline Executed Successfully.");
        System.out.println("=========================================================================");
    }
}
