@portal @tc3
Feature: Create a new service
  This feature tests the portal functionality for creating a new service with success response

  @createService
  Scenario: Create a new service: Reject
    Given I set data values against testcase "4"
    And I set BI "controller" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    And I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    Then Validate that "operationType" should be "create service"
    And Validate that "operationResult" should be "REJECTED"
    And Validate the "error" message is same as returned earlier
    And I click on "HistoryButton" and "History" Modal should open
    Then Validate that History Modal "OperationResultValue" should be "REJECTED"
    And "userID" should be available in "User ID" column for latest transaction