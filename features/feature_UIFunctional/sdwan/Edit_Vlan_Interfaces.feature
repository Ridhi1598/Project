@vlanInterfaces @vlan
Feature: Edit VLAN
  This feature tests the functionality related to editing a VLAN

    Background:
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then Validate that all customers on VCO are listed
      And I filter and select a customer

  @editVLANOneInterface
    Scenario: Edit attributes of VLAN mapped to only one Interface
      Given wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"
      Then I Navigate to the Devices Link and filter a device for Delete VLAN Scenerio
      And Select a Device and Navigate to the DeviceConfigPage
      Then I go to "DeviceConfig"
      When I click on "VLANs" button
      Then I click on "addVLAN" button
      Then "AddVLAN" page title should contain "Add VLAN"
      And Fill the required parameter to add a VLAN under "GE1" Interface
      When Navigate to commit view
      When "VLANReview" page title should contain "Review and Commit"
      When I click on "Commit" button
      Then Validate VLAN is added to VLAN table on portal
      Then Edit attributes of Vlan mapped to only "one" interface
      Then Validate updated values for Vlan that mapped to only one/multiple interface

 @editVLANMultipleInterface @multiple
    Scenario: Edit attributes of VLAN mapped to multiple Interface
      Given wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"
      And I Navigate to the Devices Link and filter a device for Delete VLAN Scenerio
      And Select a Device and Navigate to the DeviceConfigPage
      Then I go to "DeviceConfig"
      When I click on "VLANs" button
      Then I click on "addVLAN" button
      Then "AddVLAN" page title should contain "Add VLAN"
      And Fill the required parameter to add a VLAN under "GE1" Interface
      When Navigate to commit view
      Then "VLANReview" page title should contain "Review and Commit"
      When I click on "Commit" button
      Then Validate VLAN is added to VLAN table on portal
      And I go to "LANInterfaces"
      And I navigate to the provided interface for "delete_vlan_GE2" scenario
      Then Validate the delete VLAN mapped to multiple interface
      Then Review and commit for "delete_vlan_GE2" interface
      Then Edit attributes of Vlan mapped to only "multiple" interface
      Then Validate updated values for Vlan that mapped to only one/multiple interface