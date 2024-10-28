Feature: Delete VLAN Successfully
  This feature tests the functionality related to Delete VLAN

    Background:
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer
      And wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"
      Then I Navigate to the Devices Link and filter a device for Delete VLAN Scenerio
      And Select a Device and Navigate to the DeviceConfigPage
      And I go to "DeviceConfig"
      And I click on "VLANs" button
      When I click on "addVLAN" button
      Then "AddVLAN" page title should contain "Add VLAN"

@deleteVLAN
    Scenario: Delete VLAN mapped to multiple interface
      Given Fill the required parameter to add a VLAN under "GE1" Interface
      When Navigate to commit view
      Then "VLANReview" page title should contain "Review and Commit"
      And I click on "Commit" button
      When Validate VLAN is added to VLAN table on portal
      Then I go to "LANInterfaces"
      Then I navigate to the provided interface for "delete_vlan_GE2" scenario
      And Validate the delete VLAN mapped to multiple interface
      Then Review and commit for "delete_vlan_GE2" interface
      Then Delete the VLAN mapped to multiple Interface

@deleteVLAN
    Scenario: Delete VLAN mapped to one interface
      Given Fill the required parameter to add a VLAN under "GE3" Interface
      When Navigate to commit view
      Then "VLANReview" page title should contain "Review and Commit"
      And I click on "Commit" button
      Then Validate VLAN is added to VLAN table on portal
      Then Delete the VLAN mapped to one Interface
