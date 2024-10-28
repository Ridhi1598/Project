@addDevice
Feature: Add Device(CPE)
  This feature tests the functionality related to adding a CPE device

Background:
    Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer
      And wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"

@addDevice
    Scenario: Add a CPE device successfully
      Then Click on "devicesURL" and wait for the devices page
      When "AddNewDevice" page title should contain "Add New Device"
      Then Fill the required parameter to add a new device for "modelE3800Val"
      Then I perform Commit operation to add a new Device for "modelE3800Val"
      Then Validate that the added device for "modelE3800Val" is shown on portal

@addDevice
    Scenario: Add a CPE device successfully
      Then Click on "devicesURL" and wait for the devices page
      When "AddNewDevice" page title should contain "Add New Device"
      Then Fill the required parameter to add a new device for "modelE610Val"
      Then I perform Commit operation to add a new Device for "modelE610Val"
      Then Validate that the added device for "modelE610Val" is shown on portal

