Feature: Check RollBack config delete MWR scenario
  This feature tests RollBack config Scenarios for the delete MWR

  Scenario: RollBack config delete MWR Operation
    Given I set data values against testcase "56"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then I click on "HistoryButton" and "History" Modal should open
    And Validate RollBack config button should be available on action column
    Then I click on "RollBackButton" button
    Then I Wait for the Rollback Configuration Information to appear
    And Validate that mwr device is not available in Rollback Configuration Information
    Then I click on Close History Modal button