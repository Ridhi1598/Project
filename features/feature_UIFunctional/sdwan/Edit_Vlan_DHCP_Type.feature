@editVLAN @vlan
Feature: Edit VLAN
  This feature tests the functionality related to editing a VLAN

    Background:
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then Validate that all customers on VCO are listed
      And I filter and select a customer

  @editVLANenabled
    Scenario: Edit scenario wrt DHCP state enabled
      Given "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "devices"
      Then "CustomerDevice" page title should contain "Devices"
      Then I filter and select a Device
      And Navigate to "DeviceConfig" view
      When I click on "VLANs" button
      Then I filter and select a VLAN
      And I click on "Edit" button
      And "EditVLAN" page title should contain "Edit VLAN"
      When Edit the required VLAN parameters for DHCP state "Enabled"
      Then I save and commit the changes
      And "VLANReview" page title should contain "Review and Commit"
      When I click on "Commit" button
      Then Validate VLAN updates are shown on VLAN table on portal

@editVLANdisabled
    Scenario: Edit scenario wrt DHCP state disabled
      Given "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "devices"
      Then "CustomerDevice" page title should contain "Devices"
      Then I filter and select a Device
      And Navigate to "DeviceConfig" view
      When I click on "VLANs" button
      Then I filter and select a VLAN
      When I click on "Edit" button
      Then "EditVLAN" page title should contain "Edit VLAN"
      And Edit the required VLAN parameters for DHCP state "Disabled"
      When I save and commit the changes
      Then "VLANReview" page title should contain "Review and Commit"
      And I click on "Commit" button
      And Validate VLAN updates are shown on VLAN table on portal

@editVLANrelay
    Scenario: Edit scenario wrt DHCP state relay
      Given "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "devices"
      Then "CustomerDevice" page title should contain "Devices"
      And I filter and select a Device
      And Navigate to "DeviceConfig" view
      When I click on "VLANs" button
      Then I filter and select a VLAN
      And I click on "Edit" button
      And "EditVLAN" page title should contain "Edit VLAN"
      And Edit the required VLAN parameters for DHCP state "Relay"
      And I save and commit the changes
      When "VLANReview" page title should contain "Review and Commit"
      Then I click on "Commit" button
      Then Validate VLAN updates are shown on VLAN table on portal