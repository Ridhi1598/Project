#noinspection CucumberUndefinedStep
Feature: Add an Audit Job
  This feature tests the functionalities related to adding an audit job

Background:
    Given I should land on Home page
    When "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    Then I navigate view by clicking on "AuditRemediation"

    @addAuditJobError
    Scenario: Add an audit job to return error
        Given Go to the AddAuditJob page
        When "AddAuditJob" page title should be "ADD AUDIT JOB"
        Then Select "AAA" feature to Audit Job
        Then Add Audit Job "auditJobName" and "auditJobDescription"
        Then Filter devices to perform audit by using "filterDeviceName"
        Then "selectDevices" to Audit and click on "addDevicesToJob" Button
        Then Click on "proceedToScheduleJob" Button to open the Scheduling view
        Then title of "chooseAuditSchedule" should be "CHOOSE AUDIT SCHEDULE"
        Then validate "doNotSchedule" should be selected
        Then title of "confirmAuditJobTitle" should be "CONFIRM AUDIT JOB"
        Then click on "confirmAuditButton" and validate "auditName"
        Then I click on Ok button to add audit job
        And Validate the Run Audit button & Job Name
        And navigate to the view by clicking "linkRunRemediateJobs"
        And Filter the jobs by audit job name

    @addAuditJobFailure
    Scenario: Add an audit job to return failure
        Given Go to the AddAuditJob page
        When "AddAuditJob" page title should be "ADD AUDIT JOB"
        Then Select "services" feature to Audit Job
        Then Add Audit Job "auditJobName" and "auditJobDescription"
        Then Filter devices to perform audit by using "filterDeviceName"
        Then "selectDevices" to Audit and click on "addDevicesToJob" Button
        Then Click on "proceedToScheduleJob" Button to open the Scheduling view
        Then title of "chooseAuditSchedule" should be "CHOOSE AUDIT SCHEDULE"
        Then validate "doNotSchedule" should be selected
        Then title of "confirmAuditJobTitle" should be "CONFIRM AUDIT JOB"
        Then click on "confirmAuditButton" and validate "auditName"
        Then I click on Ok button to add audit job
        And Validate the Run Audit button & Job Name
        And navigate to the view by clicking "linkRunRemediateJobs"
        And Filter the jobs by audit job name

    @addAuditJobSuccess
    Scenario: Add an audit job to return success
        Given Go to the AddAuditJob page
        When "AddAuditJob" page title should be "ADD AUDIT JOB"
        Then Select "ipBase" feature to Audit Job
        Then Add Audit Job "auditJobName" and "auditJobDescription"
        Then Filter devices to perform audit by using "filterDeviceName"
        Then "selectDevices" to Audit and click on "addDevicesToJob" Button
        Then Click on "proceedToScheduleJob" Button to open the Scheduling view
        Then title of "chooseAuditSchedule" should be "CHOOSE AUDIT SCHEDULE"
        Then validate "doNotSchedule" should be selected
        Then title of "confirmAuditJobTitle" should be "CONFIRM AUDIT JOB"
        Then click on "confirmAuditButton" and validate "auditName"
        Then I click on Ok button to add audit job
        And Validate the Run Audit button & Job Name
        And navigate to the view by clicking "linkRunRemediateJobs"
        And Filter the jobs by audit job name

    @addAuditJob @parallel
     Scenario: Add an audit job and Run Audit immediately
        Given Go to the AddAuditJob page
        When "AddAuditJob" page title should be "ADD AUDIT JOB"
        Then Select "logging" feature to Audit Job
        Then Add Audit Job "auditJobName" and "auditJobDescription"
        Then Filter devices to perform audit by using "filterDeviceName"
        Then "selectDevices" to Audit and click on "addDevicesToJob" Button
        Then Click on "proceedToScheduleJob" Button to open the Scheduling view
        Then title of "chooseAuditSchedule" should be "CHOOSE AUDIT SCHEDULE"
        Then Select option "runAuditImmediately" to add audit job
        Then Select Audit Option and format
        Then Click on "proceedToConfirmAuditJob" button to open Confirm Audit Job page
        Then Click on Ok button to commit add audit job by run remediation
        Then Validate the audit status
        And navigate to the view by clicking "linkRunRemediateJobs"
        And Filter the jobs by audit job name

  @addAuditJobAllFeatures @parallel
   Scenario: Add an audit job to include all features
      Given Go to the AddAuditJob page
      When "AddAuditJob" page title should be "ADD AUDIT JOB"
      Then Select all features to be added in the audit job
      Then Add Audit Job "auditJobName" and "auditJobDescription" for all features
      Then Filter devices to perform audit by using "filterDeviceName"
      Then "selectDevices" to Audit and click on "addDevicesToJob" Button
      Then Click on "proceedToScheduleJob" Button to open the Scheduling view
      Then title of "chooseAuditSchedule" should be "CHOOSE AUDIT SCHEDULE"
      Then validate "doNotSchedule" should be selected
      Then title of "confirmAuditJobTitle" should be "CONFIRM AUDIT JOB"
      Then click on "confirmAuditButton" and validate "auditName" for all features
      Then I click on Ok button to add audit job
      And Validate the Run Audit button & Job Name for all features
      And navigate to the view by clicking "linkRunRemediateJobs"
      And Filter the jobs by audit job name for all features