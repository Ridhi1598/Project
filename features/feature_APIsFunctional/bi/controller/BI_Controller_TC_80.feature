@controller @rmq
Feature: Validate controller response for update service
  This features validates controller response for updating only speed parameter

  Scenario: Update only speed for an existing service get success
    Given I set BI "controller" url
    And I set data values against test case "80"
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
    And Validate the service record for expected "id" and "state"
	And Validate the service record for expected "in_progress" state

  Scenario: Executing an update request originating from TINAA
    Given I generate access token for authorization
    And I set BI "controller" url
    And I set data values against test case "58"
     And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body should have "status" as "success"
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue

  Scenario: Update only speed for an existing service get success
    Given I set data values against test case "80"
    And Mock "success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    And Validate the service record for expected "id" and "stateChange"
    And Validate the service record for expected "in_progressChange" state
    And I validate that a "request" record is found in "bi-controller-requests" index
    And Validate that request "state" is "completed"
    And I Set query parameters for controller request for "before"
    And Validate that the "user_id" is same as the query parameter
    And Validate that no callback is sent to PubSub