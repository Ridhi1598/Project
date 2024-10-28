#noinspection CucumberUndefinedStep
Feature: Review Device Parameters
  This feature tests the functionalities related to reaviewing device parameters

  @reviewParameters
  Scenario: Review Device Parameters at Customer Level
    Given I should land on Home page
    Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    Given I navigate view by clicking on "ManageAuditConfigs"
    Given "ManageAuditConfigs" page title should be "MANAGE AUDIT CONFIGURATIONS"
    When Select a customer and navigate to "DeviceTab"
    When Filter and select a device
    When Set parameters for "Customer Router IP"
    When I perform commit action
    When I refresh the page
    Then Validate that the modified values for "Customer Router IP" are displayed