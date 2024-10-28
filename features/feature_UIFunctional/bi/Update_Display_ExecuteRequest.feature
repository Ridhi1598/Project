Feature: Update Parameter Information for a service
  This feature tests the functionality for update parameters information

@update @display @execute
  Scenario: Update Service Request Successfully
    Given I set data values against testcase "2"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then Search the selected service ID and click on the result
    And Update the required values of parameter information for "success" scenario
    And Wait for next page to load and validate the configurations for "success" scenario
    And I click on "AcceptContinueButton" button
    And I fill the required parameters for Execution details form
    And I validate the request is successfully updated
    And Status should be updated for "AcceptContinue" in the BI service dashboard table