#noinspection CucumberUndefinedStep
  Feature: Review Audit Result
    This feature tests the functionality related to reviewing audit result

    Background:
      Given I should land on Home page
      When "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
      Then I navigate view by clicking on "AuditRemediation"
      Then I navigate view by clicking on "RunRemediateJobs"
      Then "RunRemediateAuditJobs" page title should be "RUN & REMEDIATE AUDIT JOBS"

    @reviewAuditResultError
    Scenario: Audit Job returns Error
      Then Search the Audit job for "Error" scenario by name and select the first job
      Then Select the Audit dropdown and click on Audit report
      Then Validate that the error message is as expected

    @reviewAuditResultSuccess
    Scenario: Audit Job is Successfully completed
      Then Search the Audit job for "Success" scenario by name and select the first job
      Then Select the Audit dropdown and click on Audit report
      Then Validate that the message is as expected

    @reviewAuditResultFailure
    Scenario: Audit Job is Failed
      Then Search the Audit job for "Failure" scenario by name and select the first job
      Then Select the Audit dropdown and click on Audit report
      Then Validate that the deviation is as expected
