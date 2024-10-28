@portal @tc16
Feature: Create a new service
  This feature tests the portal functionality for creating a new service with failed response

  @createService
  Scenario: Create a new service-Failed
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
    When I "start" zookeeper connectivity for node validation
    And I validate that a "node" is "created" in zookeeper instance
    Given I should land on "Home" page
    When "Home" page title should be "Services"
    Then I wait for the "current page" to load
    Then I search for "serviceId" parameter through "advanceFilter"
    And Wait for the "serviceId" search results to appear
    And Validate that "OperationType" value should be "CREATE_SERVICE"
    And Validate that "Status" value should be "submitted"
    And Validate that "Origin" value should be "NC"
    And Validate that "User" value should be "expectedValue"
    Then Validate that the "new" generated "requestId" is displayed
    And Mock "failed" response to "RMQ" "tinaa-callbacks-tests" queue
    And I refresh the page and wait for the dashboard to load
    And I validate that a "node" is "deleted" in zookeeper instance
    When I "stop" zookeeper connectivity for node validation
    Then I search for "serviceId" parameter through "advanceFilter"
    And Wait for the "serviceId" search results to appear
    And Validate that "OperationType" value should be "CREATE_SERVICE"
    And Validate that "Status" value should be "submitted"
    When I click to "expand" the "parameter information"
    Then Validate that correct "serviceId" value is displayed
# Temp step for waiting
    Then Wait for "90" seconds


    When I set "mock-server" url
    And I send request to fetch "callback" response for "success"
    Then I validate the "callback" response format for "error" message
    And Validate that the callback info has expected "correlationId" value
    And Validate that the callback info has expected "status" value
    And Validate that the callback info has expected "code" value

  Scenario: Send request to delete callback responses from records
    When I send request to "delete" "callback" record from "mock-server"
    And I send request to fetch "callback" response for "failure"

#  Add steps for progress bar, service under services
