@controller
Feature: Validate controller response for display rollback config but request fails
  This features validates controller response for display rollback config but request fails

@displayRollbackConfig
  Scenario: rollback config but request fails
    Given I generate access token for authorization
    And I set BI "controller" url
    And I set data values against test case "74"
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate response body should have "status" as "in-progress"
    And Mock "display-rollback-config-failed" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I Set query parameters for controller request for "after"
    And I Send HTTP request for controller
    And I validate the response schema
    And I validate response body should have "rollback-config" as expected response