@portal @tc1
Feature: Create a new service
  This feature tests the portal functionality for creating a new service with failed response

  @createService
  Scenario: Create a new service: Failed
    Given I set data values against testcase "1"
    And I read service id for UI testcase
    And I set BI "controller" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I extract response value for expected "requestId"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "create service"
    And Validate that "operationResult" should be "SUBMITTED"
    Then Validate that the "new" generated "RequestID" is displayed in "dashboard"
    And Assert that "progressBar" is displayed
    When I click on "HistoryButton" and "History" Modal should open
    Then Validate that the "new" generated "RequestID" is displayed in "historyModal"
    And Validate Origin of the service should be "NC"
    And Mock "failed" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I refresh the page and wait for the dashboard to load
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "create service"
    And Validate that "operationResult" should be "FAILED"
    But Assert that "progressBar" button is not displayed
    When I click on "HistoryButton" and "History" Modal should open
    Then Validate that History Modal "OperationResultValue" should be "FAILED"
    Then Validate that the "new" generated "RequestID" is displayed in "historyModal"
    And "userID" should be available in "User ID" column for latest transaction
    But Assert that "RollBack" button is not displayed
    Then I click on "HistoryCloseButton" button
    And Open "Parameter Information" box by expanding the row
    Then Validate parameter information should be available