#noinspection CucumberUndefinedStep
Feature: Review Onboarding Result
  This feature tests the functionalities related to reviwing onboarding result

  @reviewOnboardingResult
  Scenario: Review Onboarding Result of the job
    Given I should land on Home page
    Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    Given I navigate view by clicking on "Run/ManageJobs"
    Given "Run&ManageOnboardingJobs" page title should be "RUN & MANAGE ONBOARDING JOBS"
    When Filter and select the onboarding jobs for "Success"
    When "BrownfieldOnboardingJob" page title should be "BROWNFIELD ONBOARDING JOB"
    When "ViewBrownfieldOnboardingResultStatus" value should be "Available" or "Complete" but not "Ready"
    When I click on "ViewBrownfieldOnboardingResult" button
    When Wait for OnboardingResult page to load
    When "BrownfieldOnboardingResult" page title should be "BROWNFIELD ONBOARDING RESULT"
    Then Results should be displayed in rows with columns for "Device Name", "Rule id", "Error"  and "Message"
