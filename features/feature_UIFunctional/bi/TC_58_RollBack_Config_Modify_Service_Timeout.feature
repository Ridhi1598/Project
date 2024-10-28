Feature: RollBack Display Config Operation
  This feature tests the functionality of RollBack Display Config and validation

  Scenario: RollBack Display Config Operation
    Given I set data values against testcase "58"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "rollback service"
    And Validate that "operationResult" should be "COMPLETED"
    And I search for the "old" "RequestID" for "rollback" scenario from dashboard
    When I click on "HistoryButton" and "History" Modal should open
    Then I validate the "old" "RequestID" for "rollback" scenario in history modal
    Then I click on "RollbackExpand" button
    And Wait for the expected timeout value for service
    And Validate that "rollback" config has response as "expectedValue"
    And Assert that "rollbackConfigRetry" is displayed
    And I click on "HistoryCloseButton" button