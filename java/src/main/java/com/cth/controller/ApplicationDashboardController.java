package com.cth.controller;

import com.cth.model.JobApplication;
import com.cth.service.LinkedInBotService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * Spring Boot REST Controller providing web dashboard endpoints for applied jobs.
 */
@RestController
@RequestMapping("/api/applications")
public class ApplicationDashboardController {

    private final LinkedInBotService botService;

    public ApplicationDashboardController(LinkedInBotService botService) {
        this.botService = botService;
    }

    @GetMapping
    public List<JobApplication> listAppliedJobs() {
        return botService.getAllApplications();
    }
}
