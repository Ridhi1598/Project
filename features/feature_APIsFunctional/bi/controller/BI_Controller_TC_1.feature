@controller @accessToken
Feature: Validate controller response for service request
  This features validates controller response for missing token

  Scenario: Without Access Token
    Given I set BI "controller" url
    And I set data values against test case "1"
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    Then I validate response body should have "status" as "error"
    And I validate response body should have "reason" as "Access token missing or invalid"