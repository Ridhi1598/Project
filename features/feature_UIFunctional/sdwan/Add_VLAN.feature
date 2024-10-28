@addVLAN
Feature: Add VLAN
   This feature tests the functionality related to ADD VLAN

     Background:
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then I filter and select a customer

 @addVLANdisabledInterface
     Scenario: Add VLAN Successfully for disabled interface
      Given wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"
      And I Navigate to the Devices Link and filter a device by name
      And Select a Device and Navigate to the DeviceConfigPage
      When I go to "LANInterfaces"
      Then I navigate to the provided interface for "disable" scenario
      Then Disable the selected Interface
      And Review and commit the "disable" interface
      And I go to "DeviceConfig"
      When I click on "VLANs" button
      Then I click on "addVLAN" button
      Then "AddVLAN" page title should contain "Add VLAN"
      And Fill the required parameter to add a VLAN under "GE3" Interface
      And Navigate to commit view
      And "VLANReview" page title should contain "Review and Commit"
      When I click on "Commit" button
      Then Validate VLAN is added to VLAN table on portal

 @addVLANaccessInterface
     Scenario: Add VLAN Successfully for access interface
      Given wait till the Customer HomePage is loaded
      When "CustomerHome" page title should be "Customer Home"
      Then I go to "CustomerDevice"
      And I Navigate to the Devices Link and filter a device by name
      And Select a Device and Navigate to the DeviceConfigPage
      When I go to "LANInterfaces"
      Then I navigate to the provided interface for "access" scenario
      And Validate the state of selected Interface
      And Review and commit the "access" interface
      And I go to "DeviceConfig"
      When I click on "VLANs" button
      Then I click on "addVLAN" button
      Then "AddVLAN" page title should contain "Add VLAN"
      And Fill the required parameter to add a VLAN under "GE1" Interface
      And Navigate to commit view
      And "VLANReview" page title should contain "Review and Commit"
      When I click on "Commit" button
      Then Validate VLAN is added to VLAN table on portal