@editLAN_4 @lan
Feature: Edit LAN Interface
  This feature tests the functionality related to Edit LAN Interface

Background:
    Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer
      And wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"

@editLANInterface @lan7
    Scenario: Switch an access mode interface to different Vlan
      Given I Navigate to the Devices Link and filter a device for edit LAN Interface
      When Select a Device and Navigate to the DeviceConfigPage
      Then I go to "LANInterfaces"
      And I navigate to the provided interface for "switch_AD" scenario
      Then Validate the selected Interface for switching the mode from access to trunk
      And Review and commit for "switch_AD" interface
      And Add a VLAN under "GE3" Interface
      Then I go to "LANInterfaces"
      And Switch an access mode interface to a different VLAN for access mode