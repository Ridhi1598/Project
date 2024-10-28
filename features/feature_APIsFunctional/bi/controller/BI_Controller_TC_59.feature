@controller
Feature: Validate controller response for executing a request in invalid state
  This features validates controller response for executing a request in invalid state

@update
  Scenario: Executing an update request in invalid state
    Given I generate access token for authorization
    And I set BI "controller" url
    And I set data values against test case "59"
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body for expected "status" and "reason"
    Then I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
	And Validate the service record for expected "in_progress" state
    And Validate that the request is "not" in "service queue"
    And I validate that a "request" record is found in "bi-controller-requests" index
    And Validate that request "state" is not "pending"