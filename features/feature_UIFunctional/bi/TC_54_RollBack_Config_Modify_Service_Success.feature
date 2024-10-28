Feature: RollBack Display Config Operation
  This feature tests the functionality of RollBack Display Config and validation

  Scenario: RollBack Display Config Operation
    Given I set data values against testcase "54"
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
    And Wait for "10" seconds
    Then i click on "rollbackConfigRetry" button
    And I set BI "controller" url
    And I Set api endpoint and request Body
    And Mock "display-rollback-config-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And Validate that "rollback" config has response as "expectedValue"
    And I click on "HistoryCloseButton" button