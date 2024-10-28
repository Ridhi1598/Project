#noinspection CucumberUndefinedStep
Feature: Activate Device
  This feature tests the functionality related to activating a CPE device

@activateDevice
    Scenario: Activate a CPE device successfully
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer
      And "CustomerHome" page title should be "Customer Home"
      And Navigate to sidebar link "devices"
      And "CustomerDevice" page title should contain "Devices"
      When I filter and select a Device
      Then Validate that device status should be "deactivated" or "pending"
      Then I navigate to "Activate" button
      Then Fill the required parameters for Device activation
      Then Validate that activation email is sent to the test account

