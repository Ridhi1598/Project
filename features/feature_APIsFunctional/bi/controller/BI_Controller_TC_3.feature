@controller

Feature: Validate controller response for create service
  This features validates controller response for creating a failed service request

  Scenario: Create service with valid payload and service but fails
    Given I set BI "controller" url
    And I set data values against test case "3"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body for expected "status" and "reason"
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    And Validate the service record for expected "id" and "state"
    And Validate the service record for "in_progress" state to be "true"