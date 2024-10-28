@controller @rmq
Feature: Validate controller response for update service
  This features validates controller response for updating only speed parameter

  Scenario: Remove ipv4 customer prefixes for an existing ipv6 service
    Given I set BI "controller" url
    And I set data values against test case "106"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body for expected "status"
    And I validate response body for expected "reason"
    And I validate response body for expected "code"
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    And Validate the service record for expected "id" and "state"
