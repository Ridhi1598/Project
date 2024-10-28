#noinspection CucumberUndefinedStep
Feature: Display Customers
  This feature tests the functionality related to displaying customers

@displayCustomers
    Scenario: All customers on VCO should be listed
      Given I should land on SDWAN portal
      When "SDWANHome" page title should be "SD-WAN Customers"
      Then Validate that all customers on VCO are listed