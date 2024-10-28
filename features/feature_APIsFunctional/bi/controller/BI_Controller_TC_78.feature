@controller
Feature: Validate controller response for create service
  This features validates controller response for creating a service with invalid prefix value

  Scenario: Create service with invalid payload
    Given I set BI "controller" url
    And I set data values against test case "78"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body for expected "status" and "reason"
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    And Validate the service record for expected "id" and "state"