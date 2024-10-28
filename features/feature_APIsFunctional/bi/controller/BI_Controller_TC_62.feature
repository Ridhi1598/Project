@controller
Feature: Validate controller response for display before and after config for an update request
  This features validates controller response for display before and after config for an update request

@update
  Scenario: Updating a service request
    Given I set BI "controller" url
    And I set data values against test case "50"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And Validate that a new request id is returned
    And Validate that the request id has "updated" parameters

@displayConfig
  Scenario: Display before and after config for an update request
    Given I generate access token for authorization
    And I set BI "controller" url
    And I set data values against test case "62"
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