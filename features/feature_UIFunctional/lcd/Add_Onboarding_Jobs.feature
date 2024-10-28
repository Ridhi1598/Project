#noinspection CucumberUndefinedStep
Feature: Add Device Onboarding Jobs
  This feature tests the functionality related to adding an onboarding job

    @addOnboardingJobs, @demo
    Scenario: Add Onboarding Jobs
      Given I should land on Home page
      Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
      Given I navigate view by clicking on "AddBrownfieldJob"
      Given "AddBrownfieldJob" page title should be "ADD BROWNFIELD ONBOARDING JOB"
      When Filter device(s) to onboard
      When Select device(s) to onboard
      When Validate that device is not onboarded already
      When I click on "AddDevicesToJob" button
      When I click on "ProceedtoConfirmJob" button
      When "ConfirmBrownfieldOnboardingJob" page title should be "CONFIRM BROWNFIELD ONBOARDING JOB"
      When Enter Onboarding Job Name and Description
      When I click on "ConfirmOnboardingJob" button
      Then Wait for the onboarding job to be added
      Then "BrownfieldOnboardingJob" page title should be "BROWNFIELD ONBOARDING JOB"
      Then Validate that the job is added and listed