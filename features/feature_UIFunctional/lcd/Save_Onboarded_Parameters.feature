#noinspection CucumberUndefinedStep
Feature: Save Onboarded parameters
  This feature tests the functionality related to saving onboarding parameters

  @saveOnboardedParameters
  Scenario: Save Parameters to Datastore
    Given I should land on Home page
    Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    Given I navigate view by clicking on "Run/ManageJobs"
    Given "Run&ManageOnboardingJobs" page title should be "RUN & MANAGE ONBOARDING JOBS"
    When Filter and select the onboarding jobs for "Success"
    When "BrownfieldOnboardingJob" page title should be "BROWNFIELD ONBOARDING JOB"
    When "SaveParameterstoDatastoreStatus" stage status should be displayed "Ready"
    When I click on "SaveParameterstoDatastore" button
    When I click on "YesButton" button
    Then "SaveParameterstoDatastoreStatus" stage status should become "Complete"
    Then "ReviewDeviations" stage status value should be "Available"
    Then Navigate to Manage Audit Configs page
    Then Assert that device parameters are available