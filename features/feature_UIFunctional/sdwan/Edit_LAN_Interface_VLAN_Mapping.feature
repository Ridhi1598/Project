@editLAN2 @lan
Feature: Edit LAN Interface
  This feature tests the functionality related to Edit LAN Interface

Background:
    Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer
      And wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"

  @editLANInterface @lan3
    Scenario: Edit a LAN interface by enable an disabled interface and map it to a VLAN
      Given I Navigate to the Devices Link and filter a device for edit LAN Interface
      When Select a Device and Navigate to the DeviceConfigPage
      And I go to "LANInterfaces"
      Then I navigate to the provided interface for "ED_access" scenario
      When Enable an disabled interface and map it to a access mode
      Then Review and commit for "ED_access" interface
      Then Interface should go back to its previous state for "ED_access"

  @editLANInterface @lan4
    Scenario: Edit a LAN interface by enable an disabled interface and map it to a multiple VLAN
      Given I Navigate to the Devices Link and filter a device for edit LAN Interface
      When Select a Device and Navigate to the DeviceConfigPage
      Then I go to "LANInterfaces"
      And I navigate to the provided interface for "ED_trunk" scenario
      When Enable an disabled interface and map it to a access mode
      Then Review and commit for "ED_trunk" interface
      And Add a VLAN under "GE6" Interface
      And Validate the mode and added VLAN under this GE6 Interface
      And Interface should go back to its previous state for "ED_trunk"