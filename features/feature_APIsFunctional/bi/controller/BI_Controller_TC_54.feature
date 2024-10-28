@controller
Feature: Validate controller response for cancelling an update request originating from NC
  This features validates controller response for cancelling an update request originating from NC

@cancel
    Scenario: Cancel a pending service request originating from NC
    Given I set BI "REST" url
    And I set data values against test case "54"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body should have "status" as "success"
    Then I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
	And Validate the service record for expected "in_progress" state
    And I validate that a "request" record is found in "bi-controller-requests" index
    And I validate record format for "request" record
    And Validate that request "state" is "cancelled"
    And Validate that request "source" is "NC"
    And Validate that the "user_id" is same as the query parameter
    And Validate that the request is "not" in "service queue"
    And Validate that the request is "found" in "dashboard"