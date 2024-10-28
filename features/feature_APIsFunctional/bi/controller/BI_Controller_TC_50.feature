@controller
Feature: Validate controller response for updating an existing service through portal
  This features validates controller response for updating an existing service through portal

@update
  Scenario: Updating a service request
    Given I set BI "controller" url
    And I set data values against test case "50"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And Validate that a new request id is returned
    And I extract response value for expected "requestId"
    And Validate that the request id has "updated" parameters
    Then I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
	And Validate the service record for expected "in_progress" state