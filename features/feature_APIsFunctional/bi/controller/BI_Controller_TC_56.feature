@controller
Feature: Validate controller response for updating a request originating from NC
  This features validates controller response for updating a request originating from NC

@update
  Scenario: Updating a service request originating from NC
    Given I generate access token for authorization
    And I set BI "REST" url
    And I set data values against test case "56"
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I extract response value for expected "requestId"
    Then I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
     And Validate the service record for expected "id" and "state"
	And Validate the service record for expected "in_progress" state
    And I validate that a "request" record is found in "bi-controller-requests" index
    And I validate record format for "request" record
    And Validate that request "state" is "pending"