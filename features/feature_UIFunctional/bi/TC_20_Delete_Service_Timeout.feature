@portal @tc20
Feature: Delete an existing service
  This feature tests the portal functionality for deleting an existing service with no callback response

  Scenario: Delete an existing service : Success
    Given I set data values against testcase "20"
    When I read service id for UI testcase
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
    And Validate that "operationType" should be "delete service"
    And Validate that "operationResult" should be "SUBMITTED"
    Then Validate that the "new" generated "RequestID" is displayed in "dashboard"
    And Assert that "progressBar" is displayed
    When I click on "HistoryButton" and "History" Modal should open
    Then Validate that the "new" generated "RequestID" is displayed in "historyModal"
    And Validate Origin of the service should be "NC"
    And Wait for the expected timeout value for service
    And I refresh the page and wait for the dashboard to load
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "delete service"
    And Validate that "operationResult" should be "TIMEOUT"
    And Assert that "progressBar" button is not displayed
    When I click on "HistoryButton" and "History" Modal should open
    Then Validate that History Modal "OperationResultValue" should be "TIMEOUT"
    Then Validate that the "new" generated "RequestID" is displayed in "historyModal"
    And "userID" should be available in "User ID" column for latest transaction
    And Assert that "RollBack" button is not displayed
    Then I click on "HistoryCloseButton" button
    When Open "Parameter Information" box by expanding the row
    Then Validate parameter information should be available