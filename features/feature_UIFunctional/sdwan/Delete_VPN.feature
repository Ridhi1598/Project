#noinspection CucumberUndefinedStep
Feature: Delete VPN
  This feature tests the functionality related to deleting a VPN

    Background:
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      When Validate that all customers on VCO are listed
      When I filter and select a customer
      When "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "networks"
      When "CustomerNetwork" page title should contain "Network View"

  @deleteVPNfail
    Scenario: Delete VPN entry failed
      Then I filter and select a network for "fail" scenario
      When I click on "deleteButton" button
      Then Validate deleting VPN with active site configurations should fail

  @deleteVPNsuccess @demo
    Scenario: Delete VPN successfully
      Then I filter and select a network for "success" scenario
      Then Verify that selected network has no active sites
      When I click on "deleteButton" button
      When I click on Yes button
      Then Validate network is removed on portal