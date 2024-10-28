@portal @tc22
Feature: Delete an existing service
  This feature tests the portal functionality for deleting an existing service which gets rejected

  Scenario: Delete an existing service : Reject
    Given I set data values against testcase "22"
    And I set BI "controller" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "delete service"
    And Validate that "operationResult" should be "REJECTED"
    And Validate the "error" message is same as returned earlier
    And I click on "HistoryButton" and "History" Modal should open
    Then Validate that History Modal "OperationResultValue" should be "REJECTED"
    And "userID" should be available in "User ID" column for latest transaction
    Then I click on "HistoryCloseButton" button
    When Open "Parameter Information" box by expanding the row
    Then Validate parameter information should be available