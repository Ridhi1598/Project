##noinspection CucumberUndefinedStep
#Feature: Deactivate Device
#  This feature tests the functionality related to deactivating a CPE device
#
#@deactivateDevice
#    Scenario: Deactivate a CPE device successfully
#      Given I should land on SDWAN portal
#      When "SDWANHome" page title should be "SD-WAN Customers"
#      When Validate that all customers on VCO are listed
#      When I filter and select a customer
#      When "CustomerHome" page title should be "Customer Home"
#      When Navigate to sidebar link "devices"
#      When "CustomerDevice" page title should contain "Devices"
#      When I filter and select a Device
#      When Validate that device status should be "active"
#      When I navigate to "Deactivate" button
#      When I click on Yes button
#      Then Validate that device status changes to Deactivated
#
#
#
#
