@editLAN1 @lan
Feature: Edit LAN Interface
  This feature tests the functionality related to Edit LAN Interface

Background:
    Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer
      And wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"

@editLANInterface @lan1
    Scenario: Edit a LAN interface by disabling access mode interface
      Given I Navigate to the Devices Link and filter a device for edit LAN Interface
      When Select a Device and Navigate to the DeviceConfigPage
      And I go to "LANInterfaces"
      Then I navigate to the provided interface for "access" scenario
      When Disable an enable interface and map it to a access mode
      Then Review and commit for "DE_access" interface
      Then Interface should go back to its previous state for "DE_access"

  @editLANInterface @lan2
    Scenario: Edit a LAN interface by disabling TRUNK mode interface
      Given I Navigate to the Devices Link and filter a device for edit LAN Interface
      When Select a Device and Navigate to the DeviceConfigPage
      Then Add a VLAN under "GE2" Interface
      And I go to "LANInterfaces"
      Then I navigate to the provided interface for "DE_trunk" scenario
      And Disable an enable interface and map it to a trunk mode
      Then Review and commit for "DE_trunk" interface
      Then Interface should go back to its previous state for "DE_trunk"
      Then filter and delete the last added VLAN for edit LAN Interface