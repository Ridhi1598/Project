#noinspection CucumberUndefinedStep
Feature: Add VPN
  This feature tests the functionality related to adding a new network

@addVPN @demo
    Scenario: Add VPN successfully
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      When I filter and select a customer
      When "CustomerHome" page title should be "Customer Home"
      When Navigate to sidebar link "networks"
      When "CustomerNetwork" page title should contain "Network View"
      When I click on addNetwork button
      When "AddNewNetwork" page title should contain "Add New Network"
      When Fill the required network parameters
      When I click on "save" button
      When "CustomerNetwork" page title should contain "Network View"
      Then Added network should be listed under the list of networks
      Then I click on "review" button
      Then "NetworkReview" page title should contain "Network: Review and Commit"
      When I click on "commit" button
      Then New network should be listed under the list of networks