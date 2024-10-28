@controller
Feature: Validate controller response for modify service if concurrent requests count exceeds Rate Limit
  This features validates controller response for modify service if concurrent requests count exceeds Rate Limit

  Scenario: Modify service against Rate Limit
    Given I set BI "controller" url
    And I set data values against test case "86"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body for expected "status" and "reason"