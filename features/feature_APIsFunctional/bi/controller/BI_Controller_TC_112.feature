@controller
Feature: Validate controller response with success message for rollback current and expected config for a rollback request
  This features validates controller response for rollback current and expected config for a rollback request

@rollback
  Scenario: Create service rollback success
    Given I set BI "controller" url
    And I set data values against test case "68"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I extract response value for expected "requestId"

@displayConfig
  Scenario: Display current and expected config for a rollback request: Timeout
    Given I generate access token for authorization
    And I set BI "controller" url
    And I set data values against test case "112"
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate response body should have "status" as "in-progress"
    And Wait for the expected timeout value for service
    And I Set query parameters for controller request for "after"
    And I Send HTTP request for controller
    And I validate the response schema
    Then I validate response body should have "current-config" as expected response
    And I validate response body should have "expected-config" as expected response