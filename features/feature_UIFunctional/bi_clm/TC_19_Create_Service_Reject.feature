@portal @tc17
Feature: Create a new service
  This feature tests the portal functionality for creating a new service with success response

  @createService
  Scenario: Create a new service-Success
    Given I read test data for testcase
    And I read service id for UI testcase
    And I set "ingestion" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "ingestion" api endpoint
    And I Set "ingestion" api request body
    And I Set query parameters for "ingestion" request for "before"
    When I Send HTTP request for "ingestion"
    And I validate the expected response schema
    And I extract response value for "error"
    Given I should land on "Home" page
    When "Home" page title should be "Services"
    Then I wait for the "current page" to load
    Then I search for "serviceId" parameter through "advanceFilter"
    And Wait for the "serviceId" search results to appear
    And Validate that "OperationType" value should be "CREATE_SERVICE"
    And Validate that "Status" value should be "rejected"
    And Validate that "Origin" value should be "NC"
    And Validate that "User" value should be "expectedValue"
    When I click on the "Status" and read "alert Modal" message