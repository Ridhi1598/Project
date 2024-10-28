Feature:Modify a service without changing any parameter from service update queue
  This feature tests the functionality of Modify service without changing any parameter from service update
  queue and validation

  Scenario: Modify a service without changing any parameter from service update queue
    Given I set data values against testcase "10"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then Search the selected service ID and click on the result
    And Update the required values of parameter information for "success" scenario
    And Wait for next page to load and validate the configurations for "success" scenario
    When "ServiceUpdateQueue" page title should be "Service Update Queue"
    Then I click on "ReviewUpdateEdit" button
    And I click on "ParameterSave" button
    And "ErrorAlertMessage" should be "The entered values should be different than the ones assigned before"