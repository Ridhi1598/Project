#noinspection CucumberUndefinedStep
   Feature: Add Tags at Customer and Device level
     This feature tests the functionality related to tags

   Background:
     Given I should land on Home page
     Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
     Given I navigate view by clicking on "AuditRemediation"

      @customerTags
      Scenario: Add customer tags and filter device for onboarding job
        When I navigate view by clicking on "ManageAuditConfigs"
        When "ManageAuditConfigurations" page title should be "MANAGE AUDIT CONFIGURATIONS"
        And Click on "Customers" and filter the customer by "filterCustomerName"
        And Add corresponding tags to selected customer and click submit
        Then Navigate to "deviceOnboarding" and click on "addBrownfieldJob"
        Then validate the correct device is filterd by using Customer Tag
        Then I perform Commit action

      @deviceTags
      Scenario: Add device tags and filter device for audit jobs
        When I navigate view by clicking on "ManageAuditConfigs"
        Then "ManageAuditConfigurations" page title should be "MANAGE AUDIT CONFIGURATIONS"
        When Click on "Customers" and filter the customer by "filterCustomerName"
        When go to device level by "devicesButton"
        When Add corresponding tags to selected device
        Then clicking on "addAuditJob"
        Then validate that the result is as expected based on device tag
        Then I perform Commit action