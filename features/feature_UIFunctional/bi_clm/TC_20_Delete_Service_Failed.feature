@portal @tc20
Feature: Delete an Existing Service
  This feature tests the portal functionality for deleting an existing service with failed response

  @createService
  Scenario: Delete an Existing Service-Failed
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
    And I extract response value for "requestId"
    Given I should land on "Home" page
    When "Home" page title should be "Services"
    Then I wait for the "current page" to load
    Then I search for "serviceId" parameter through "advanceFilter"
    And Wait for the "serviceId" search results to appear
    And Validate that "OperationType" value should be "DELETE_SERVICE"
    And Validate that "Status" value should be "submitted"
    And Validate that "Origin" value should be "NC"
    And Validate that "User" value should be "expectedValue"
    Then Validate that the "new" generated "requestId" is displayed
    And Mock "failed" response to "RMQ" "tinaa-callbacks-tests" queue
    And I refresh the page and wait for the dashboard to load
    Then I search for "serviceId" parameter through "advanceFilter"
    And Wait for the "serviceId" search results to appear
    And Validate that "OperationType" value should be "DELETE_SERVICE"
    And Validate that "Status" value should be "failed"
    When I click to "expand" the "parameter information"
    Then Validate that correct "serviceId" value is displayed
    When I navigate to "Services" view
    When "Services" page title should be "Services"
    Then I wait for the "current page" to load
    Then I search for "serviceId" parameter through "advanceFilter"
    And Wait for the "serviceId" search results to appear

#  Add steps for progress bar