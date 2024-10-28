@controller
Feature: Validate controller response for display rollback config for a deleted service
  This features validates controller response for display rollback config for a deleted sister

@displayRollbackConfig
  Scenario: Display rollback config for a deleted service
    Given I generate access token for authorization
    And I set BI "controller" url
    And I set data values against test case "117"
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate response body should have "status" as "in-progress"
    And I validate response body should have "rollback-config" as expected response
    And I validate the response schema