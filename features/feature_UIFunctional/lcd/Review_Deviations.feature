Feature: Review Deviations
  This feature tests the functionality related to review deviations

    Background:
      Given I should land on Home page
      Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"

      @updateCustomerStandardViaReviewDeviation @RR
      Scenario: Update Standards from Review Deviations view
        When I navigate view by clicking on "Run/ManageJobs"
        When "Run&ManageOnboardingJobs" page title should be "RUN & MANAGE ONBOARDING JOBS"
        When Filter and select the onboarding job for Update Standards
        When "BrownfieldOnboardingJob" page title should be "BROWNFIELD ONBOARDING JOB"
        When "ReviewDeviations" stage status value should be "Available"
        When I click on "ReviewDeviationsBtn" button
        When "DeviationsReview" page title should be "DEVIATIONS REVIEW"
        When "searchintable" the parameter "logging-server" for review and select "UpdateStandard"
        And Wait for popup and click on "acceptDeviationsButton" button
        Then Navigate to manage audit configs
        Then "ManageAuditConfigs" page title should be "MANAGE AUDIT CONFIGURATIONS"
        Then Navigate to the device view and search for "logging" to assert
        Then go to the "linkCustomerGroup" and select the Customer Group
        Then I validate the logging server value

      @AcceptDeviationsViaManageAuditConfigs
      Scenario: Accept deviation from Manage Audit Configs view
        When I navigate view by clicking on "ManageAuditConfigs"
        When "ManageAuditConfigs" page title should be "MANAGE AUDIT CONFIGURATIONS"
        When Navigate to "deviationsReview" at device level
        When Search the parameter "customer-router-ip" and accept deviation
        And Wait for popup and click on "acceptDeviationsButton" button
        When Navigate to device level and assert that parameters "customer-router-ip" are accepted