Feature: Edit WAN Interface
  This feature tests the functionality related to Edit WAN Interface

  Background:
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer
      Then wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"
      And I Navigate to the Devices Link and filter a device by name
      And Select a Device and Navigate to the DeviceConfigPage
      And I go to "WANInterfaces"
      And Click on the WAN Interfaces to open EDIT/VIEW WAN Interfaces


  @editWANInterface
    Scenario: Edit a WAN interface successfully by addressing type static address
      Given Edit the WAN Interface by addressing type static address
      When Review and commit the edited parameters for Edit WAN Interface by addressing type "static address"
      Then Validate the updated parameter should be reflected on the portal for static Address

  @editWANInterface
    Scenario: Edit a WAN interface successfully by addressing type pppoe
      Given Edit the WAN Interface by addressing type pppoe
      When Review and commit the edited parameters for Edit WAN Interface by addressing type "pppoe"
      Then Validate the updated parameter should be reflected on the portal for pppoe

  @editWANInterface
    Scenario: Edit a WAN interface successfully by addressing type dhcp
      Given Edit the WAN Interface by addressing type dhcp
      When Review and commit the edited parameters for Edit WAN Interface by addressing type "dhcp"
      Then Validate the updated parameter should be reflected on the portal for dhcp
