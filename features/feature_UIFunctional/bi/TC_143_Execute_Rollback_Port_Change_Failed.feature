Feature: Execute Update Request from Service Queue
  This feature tests the functionality of executing an update request from BI Service Queue

  Scenario: Execute Port Change Request from Service Queue: Port Not Available
    Given I set data values against testcase "143"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
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
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "rollback service"
    And Validate that "operationResult" should be "SUBMITTED"
    Then Validate that the "new" generated "RequestID" is displayed in "dashboard"
    And Assert that "progressBar" is displayed
    When I click on "HistoryButton" and "History" Modal should open
    Then Validate that the "new" generated "RequestID" is displayed in "historyModal"
    And Validate Origin of the service should be "TINAA"
    And I set BI "controller" url
    And I Set api endpoint and request Body
    And Mock "port-failed" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    Then I refresh the page and wait for the dashboard to load
    And I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "rollback service"
    And Validate that "operationResult" should be "FAILED"
    And I click on "HistoryButton" and "History" Modal should open
    Then Validate that History Modal "OperationResultValue" should be "FAILED"
    And "requestId" should be available in "Request ID" column for latest transaction
    And "userID" should be available in "User ID" column for latest transaction
    But Assert that "RollBack" button is not displayed
    Then I click on "HistoryCloseButton" button
    When I click on "ParameterInformationButton" button
    Then Validate that Parameter information should be "Data Not Available!"