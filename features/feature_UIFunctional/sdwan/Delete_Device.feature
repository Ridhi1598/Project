#noinspection CucumberUndefinedStep
Feature: Delete Device

@deleteDevice
    Scenario: Delete a CPE device successfully
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      When I filter and select a customer
      When "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "devices"
      When "CustomerDevice" page title should contain "Devices"
      When I filter and select a Device to delete
      When Validate that device status should be "deactivated" or "pending"
      When I navigate to "Delete" button
      When I click on Yes button
      Then Validate device is removed on portal