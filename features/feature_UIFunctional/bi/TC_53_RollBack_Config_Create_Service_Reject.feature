Feature: Check RollBack Config Create Service scenario
  This feature tests RollBack Config Scenarios for the Create service

  Scenario: RollBack Config for create service
    Given I set data values against testcase "53"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then "OperationTypeValue" should be "rollback service"
    Then "OperationResultValue" should be "COMPLETED"
    Then I click on "HistoryButton" and "History" Modal should open
    And Validate RollBack config button should be available on action column
    Then I click on "RollBackButton" button
    Then Validate that Rollback Configuration Info should be "No Config Available - Service is already terminated "