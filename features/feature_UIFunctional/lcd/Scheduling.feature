#noinspection CucumberUndefinedStep
  Feature: Scheduling
     This feature tests the functionality related to scheduling audit runs

      @scheduleExistingJob
      Scenario: Schedule an already existing Audit Job
        Given I should land on Home page
        Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
        Given I navigate view by clicking on "Run&RemediateJobs"
        Given "Run&RemediateAuditJobs" page title should be "RUN & REMEDIATE AUDIT JOBS"
        Given Filter a device and select a job to open its audit view
        Given "AuditJob" page title should be "AUDIT JOB"
        Given Navigate to "ScheduleJob" button
        When "ScheduleJob" page title should be "SCHEDULE JOB"
        When Enter Audit Schedule details
        Then Wait for job to be added and displayed
        Then "ManageScheduledJobs" page title should be "MANAGE SCHEDULED JOBS"
        Then Validate that the scheduled job is added successfully

     @scheduleAuditJob
     Scenario: Schedule Audit job while adding Audit job
        Given I should land on Home page
        Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
        Given I navigate view by clicking on "AuditRemediation"
        Given Go to the AddAuditJob page
        Given "AddAuditJob" page title should be "ADD AUDIT JOB"
        Given Select features to be added in the audit job for scheduling
        Given Add Audit Job "auditJobName" and "auditJobDescription"
        Given Filter devices to perform audit by using "filterDeviceName"
        Given "selectDevices" to Audit and click on "addDevicesToJob" Button
        Given Click on "proceedToScheduleJob" Button to open the Scheduling view
        Given "ChooseAuditSchedule" page title should be "CHOOSE AUDIT SCHEDULE"
        When I click on "ScheduleAudit" button
        When Select Audit options and format
        When Select Audit Recurrence and fill details
        When "ConfirmAuditJob" page title should be "CONFIRM AUDIT JOB"
        When I perform Commit action
        Then I click on "ConfirmAuditJob" button
        Then Wait for page to load
        Then "AuditJob" page title should be "AUDIT JOB"
        Then Validate that Audit job is created and displayed
        Then "ManageScheduledJobs" page title should be "MANAGE SCHEDULED JOBS"
        Then Validate that the scheduled job is displayed under list of scheduled jobs


     @validateRunTime
     Scenario: Validate that scheduled job is run at the specified time
        Given I should land on Home page
        Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
        Given I navigate view by clicking on "Run&RemediateJobs"
        Given "Run&RemediateAuditJobs" page title should be "RUN & REMEDIATE AUDIT JOBS"
        Given Filter a device and select a job to open its audit view for checking runtime
        Given "AuditJob" page title should be "AUDIT JOB"
        Given Navigate to "ViewScheduledJob" button
        When "ManageScheduledJobs" page title should be "MANAGE SCHEDULED JOBS"
        Then Validate that the scheduled job is run at the specified time
        Then "Run&RemediateAuditJobs" page title should be "RUN & REMEDIATE AUDIT JOBS"
        Then Filter a device and select a job to open its audit view for checking runtime
        Then "AuditJob" page title should be "AUDIT JOB"
        Then Assert that job ran at the specified time