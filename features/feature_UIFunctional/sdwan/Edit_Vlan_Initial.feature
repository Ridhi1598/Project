@vlanInitial @vlan
Feature: Edit VLAN
  This feature tests the functionality related to editing a VLAN

    Background:
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then Validate that all customers on VCO are listed
      And I filter and select a customer

@editVLANinitial
    Scenario: Edit scenario wrt setting initial values
      Given "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "devices"
      Then "CustomerDevice" page title should contain "Devices"
      And I filter and select a Device
      And Navigate to "DeviceConfig" view
      When I click on "VLANs" button
      Then I filter and select corporate VLAN for initial setup
      When I click on "Edit" button
      And "EditVLAN" page title should contain "Edit VLAN"
      Then Edit the required VLAN parameters for DHCP state "Initial"
      Then I save and commit the changes
      And "VLANReview" page title should contain "Review and Commit"
      And I click on "Commit" button
      And Validate VLAN updates are shown on VLAN table on portal