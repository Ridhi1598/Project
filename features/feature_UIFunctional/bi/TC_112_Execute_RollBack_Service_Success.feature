Feature: Execute RollBack Request from Service Queue
  This feature tests the functionality of initiating a display rollback config call from BI Portal

  Scenario: Execute RollBack Request from Service Queue: Rollback Config Available
    Given I set data values against testcase "112"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "modify service"
    And Validate that "operationResult" should be "COMPLETED"
    And I search for the "old" "RequestID" for "rollback" scenario from dashboard
    When I click on "HistoryButton" and "History" Modal should open
    Then I validate the "old" "RequestID" for "rollback" scenario in history modal
    And I search for the "older" "RequestID" for "rollback" scenario in history modal
    And I click on "HistoryCloseButton" button
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    And Validate that service request has "Operation" as "rollback"
    And I read the "new" "requestId" for "rollback" scenario
    When I "execute" update request for selected service id
    And I fill the required parameters for Execution details form
    And An "Alert" box should open
    And I validate the "success" message in the "Alert" box for "execute"
    And I click on "OK" button
    And Validate the service is "not available" in service queue
    And I navigate view by clicking on "Dashboard"
    And "Home" page title should be "BI service dashboard"
    And I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "rollback service"
    And Validate that "operationResult" should be "SUBMITTED"
    And I set BI "controller" url
    And I Set api endpoint and request Body
    And Mock "rollback-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    Then I refresh the page and wait for the dashboard to load
    And I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "rollback service"
    And Validate that "operationResult" should be "COMPLETED"
    And I click on "HistoryButton" and "History" Modal should open
    And "requestId" should be available in "Request ID" column for latest transaction
    And "RollbackExpand" should be available in "Actions" column for latest transaction
    And "userID" should be available in "User ID" column for latest transaction
