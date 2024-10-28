Feature: RollBack Delete Service Validation
  This feature tests the functionality delete service validation


  Scenario: checking the rollback delete service validation
    Given I set data values against testcase "107"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "modify service"
    And Validate that "operationResult" should be "COMPLETED"
    And I search for the "old" "RequestID" for "rollback" scenario from dashboard
    When I click on "HistoryButton" and "History" Modal should open
    Then I validate the "old" "RequestID" for "rollback" scenario in history modal
    And "userID" should be available in "User ID" column for latest transaction
    Then "RollBackButton" button should not be available in action column