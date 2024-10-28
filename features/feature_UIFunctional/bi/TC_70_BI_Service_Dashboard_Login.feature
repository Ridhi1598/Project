@demo
Feature: BI Service Dashboard Login
  This feature tests the functionality of logging into the BI Service Dashboard

  Scenario: Log in to Bi Service Dashboard
    Given I set data values against testcase "70"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"