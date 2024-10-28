Feature: Cancel RollBack Request from Service Queue
  This feature tests the functionality of cancelling a rollback request from service queue

  Scenario: Cancel RollBack Request from Service Queue: Rollback Config Available
    Given I set data values against testcase "114"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    And Validate that service request has "Operation" as "rollback"
    And I search for the "old" "RequestID" for "rollback" scenario from dashboard
    And Click on "reviewButton" button in service queue table to open "reviewModal"
    When I click on "cancelButton" button
    And An "Confirmation" box should open
    And I validate the "confirm" message in the "Confirmation" box for "cancel"
    And I click on "Continue" button
    And An "Alert" box should open
    And I validate the "success" message in the "Alert" box for "cancel"
    And I click on "OK" button
    Then Validate the service is "not available" in service queue
    And I navigate view by clicking on "Dashboard"
    And "Home" page title should be "BI service dashboard"
    And I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "rollback service"
    And Validate that "operationResult" should be "CANCELLED"
    And I click on "HistoryButton" and "History" Modal should open
    And "requestId" should be available in "Request ID" column for latest transaction
    But "userID" should be available in "User ID" column for latest transaction
    And "RollbackExpand" should not be available in "Actions" column for latest transaction