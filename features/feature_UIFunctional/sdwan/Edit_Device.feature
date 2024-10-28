#noinspection CucumberUndefinedStep
Feature: Edit Device(CPE)
  This feature tests the functionality related to editing a CPE device

@editDevice
    Scenario: Edit a CPE device successfully
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      When I filter and select a customer
      When "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "devices"
      When "CustomerDevice" page title should contain "Devices"
      When I filter and select a Device
      When I navigate to "Edit" button
      When "EditDevice" page title should contain "Edit Device"
      When Edit the required device parameters
      When "CustomerDevice" page title should contain "Devices"
      When I filter and select updated Device
      When I navigate to "Commit" button
      When "DeviceReview" page title should contain "Review and Commit"
      When I click on "Commit" button
      Then Validate device changes are correctly displayed on portal
      Then Restore device changes to default


