Feature: Execute RollBack Request from Service Queue
  This feature tests the functionality of initiating a display rollback config call from BI Portal

  Scenario: Execute RollBack Request from Service Queue: Rollback Config In Progress
    Given I set data values against testcase "113"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "modify service"
    And Validate that "operationResult" should be "COMPLETED"
    And I search for the "old" "RequestID" for "rollback" scenario from dashboard
    When I click on "HistoryButton" and "History" Modal should open
    Then I validate the "old" Request ID for "rollback" scenario
    And "RollBack" should be available in "Actions" column for latest transaction
    Then I click on "RollBack" button
    And An "Confirmation" box should open
    And I validate the "confirm" message in the "Confirmation" box for "rollback"
    And I click on "Continue" button
    And An "Alert" box should open
    And I validate the "success" message in the "Alert" box for "rollback"
    And I click on "OK" button
    And "ServiceQueue" page title should be "Service Update Queue"
    And Assert that "reviewModal" is displayed
    And Validate that a "new" request id is generated for "rollback"
    And Validate that "old" and "new" request ids are "different" for "rollback"
    And Assert that "Edit" button is not displayed
    And Assert that response for "current" config is "In Progress ..."
    And Assert that response for "expected" config is "In Progress ..."
    When I click on "AcceptContinueButton" button
    And Validate "performButton" button should be disable
    Then I click on required parameters of Execution details form
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
    And Mock "rollback-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    Then I refresh the page and wait for the dashboard to load
    And I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "rollback service"
    And Validate that "operationResult" should be "COMPLETED"
    And I click on "HistoryButton" and "History" Modal should open
    And "requestId" should be available in "Request ID" column for latest transaction
    And "RollBackExpand" should be available in "Actions" column for latest transaction
    And "userID" should be available in "User ID" column for latest transaction