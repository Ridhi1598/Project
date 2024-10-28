@editLAN3 @lan
Feature: Edit LAN Interface
  This feature tests the functionality related to Edit LAN Interface

Background:
    Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer
      And wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"

@editLANInterface @lan5
    Scenario: Edit a LAN interface by switching access mode to the trunk
      Given I Navigate to the Devices Link and filter a device for edit LAN Interface
      When Select a Device and Navigate to the DeviceConfigPage
      Then I go to "LANInterfaces"
      And I navigate to the provided interface for "switch_AT" scenario
      And Validate the selected Interface for switching the mode from access to trunk
      And Review and commit for "switch_AT" interface
      And Add a VLAN under "GE1" Interface
      And Validate the mode and added VLAN under this GE1 Interface
      And Interface should go back to its previous state for "switch_AT"

@editLANInterface @lan6
    Scenario: Edit a LAN interface by switching trunk mode to the access
      Given I Navigate to the Devices Link and filter a device for edit LAN Interface
      When Select a Device and Navigate to the DeviceConfigPage
      Then I go to "LANInterfaces"
      And Add a VLAN under "GE2" Interface
      And I go to "LANInterfaces"
      And I navigate to the provided interface for "switch_TA" scenario
      Then Validate the selected Interface for switching the mode from trunk to access
      Then Review and commit for "switch_TA" interface