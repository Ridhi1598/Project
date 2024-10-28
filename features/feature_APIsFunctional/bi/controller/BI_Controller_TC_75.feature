@controller
Feature: Validate controller response for display rollback config but request times out
  This features validates controller response for display rollback config but request times out

@displayRollbackConfig
  Scenario: Display rollback config but request times out
    Given I generate access token for authorization
    And I set BI "controller" url
    And I set data values against test case "75"
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate response body should have "status" as "in-progress"
    And Wait for the expected timeout value for service
    And I Set query parameters for controller request for "after"
    And I Send HTTP request for controller
    And I validate the response schema
    And I validate response body should have "rollback-config" as expected response