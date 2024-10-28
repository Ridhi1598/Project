Feature: Run an Audit Job
  This feature tests the functionalities related to running an audit job

 Background:
    Given I should land on Home page
    When "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    Then I navigate view by clicking on "AuditRemediation"

  @runAuditJob @RR
  Scenario: Run an audit job successfully
    Given I navigate view by clicking on "RunRemediateJobs"
    When "RunRemediateAuditJobs" page title should be "RUN & REMEDIATE AUDIT JOBS"
    When Filter the audit jobs by "FilterDeviceName" name
    When "AuditJobSearch" the job and click on selected job to open its "AuditJobSelect" view
    When Click on "RunAudit" button to open Confirm Run Audit dialog
    Then Click on "startAudit" to open the Audit Status view
    Then Audit status displays "finishedReportReady"

  @runParallelAuditJobs @parallel
  Scenario: Run an audit job successfully
    When I navigate view by clicking on "RunRemediateJobs"
    And "RunRemediateAuditJobs" page title should be "RUN & REMEDIATE AUDIT JOBS"
    And Filter the audit jobs by "FilterDeviceName" name
    And Search the "first" job and open its Audit Job view
    Then Open a new tab and navigate to "RunRemediateJobs" page
    And "RunRemediateAuditJobs" page title should be "RUN & REMEDIATE AUDIT JOBS"
    And Search the "second" job and open its Audit Job view
    And Run the "second" job for parallel execution
    And Switch to "first" tab
    Then Run the "first" job for parallel execution
    And Wait till audit status for "first" job displays "finishedReportReady"
    Then Switch to "second" tab
    And Wait till audit status for "second" job displays "finishedReportReady"
    And Close "second" tab
    And Validate that "first" job finished before "second" job