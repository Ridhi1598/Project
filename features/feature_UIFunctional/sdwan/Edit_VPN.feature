#noinspection CucumberUndefinedStep
Feature: Edit VPN
  This feature tests the functionality related to editing a network

@editVPN @demo
    Scenario: Edit a VPN entry successfully
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      When I filter and select a customer
      When "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "networks"
      When "CustomerNetwork" page title should contain "Network View"
      Then I filter and select a network
      When I click on "editButton" button
      When "EditNetwork" page title should contain "Edit Network"
      When Change the required parameters
      When I click on "Save" button
      Then Updated network should be listed under the list of networks
      Then I click on "review" button
      Then "NetworkReview" page title should contain "Network: Review and Commit"
      Then I click on "commit" button
      Then Validate VPN changes are correctly displayed on portal
      Then Restore vpn changes to default





