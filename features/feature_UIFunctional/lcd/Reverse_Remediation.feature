  Feature: Reverse Remediation
    This feature tests the functionality related to reverse remediation

    @reverseRemediation @RR
    Scenario: Perform reverse remediation on an audit job
      Given I should land on Home page
      And "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
      And I navigate view by clicking on "AuditRemediation"
      And I navigate view by clicking on "RunRemediateJobs"
      And "RunRemediateAuditJobs" page title should be "RUN & REMEDIATE AUDIT JOBS"
      When Filter the audit job to open its Audit Job view
      And Select the Audit dropdown and click on Audit report
      And Validate that the error message is as expected
      And "AuditReport" page title should be "AUDIT REPORT"
      Then Click on "Logging" feature to open its Violations table
      And Assert that "Reverse-Remediate" is available on "Logging" rule
      And Click on "Reverse-Remediate" button to open reverse remediation results table
      And Filter "logging-server" and assert that "updateStandard" is available