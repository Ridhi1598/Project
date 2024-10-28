#noinspection CucumberUndefinedStep
Feature: Run Device Onboarding Jobs
  This feature tests the functionalities related to running onboarding job

  @runOnboardingJobSuccess
  Scenario: Run Onboarding Job Successfully
    Given I should land on Home page
    Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    Given I navigate view by clicking on "Run/ManageJobs"
    Given "Run&ManageOnboardingJobs" page title should be "RUN & MANAGE ONBOARDING JOBS"
    When Filter and select the onboarding jobs for "Success"
    When "BrownfieldOnboardingJob" page title should be "BROWNFIELD ONBOARDING JOB"
    When "OnboardBrownfieldDevicesStatus" stage status should be "Ready" and "Connected"
    Then "OnboardBrownfieldDevicesStatus" stage status should change to "Complete"
    Then "ViewBrownfieldOnboardingResultStatus" stage status value should be "Available"
    Then "SaveParameterstoDatastoreStatus" stage status value should be "Ready"

