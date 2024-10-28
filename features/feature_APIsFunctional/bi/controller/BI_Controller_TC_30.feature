@controller @rmq
Feature: Validate controller response for delete service
  This feature validates controller response for removing an MWR service successfully

  Scenario: Remove MWR service from an existing service successfully
    Given I set BI "controller" url
    And I set data values against test case "30"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I extract response value for expected "requestId"
    And I validate that a "request" record is found in "bi-controller-requests" index
    And Validate that request "state" is "submitted"
    And I validate that a "service" record is found in "bi-controller-services" index
    And Validate the service record for expected "id" and "state"
    And Validate the service record for expected "in_progress" state
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "mwr-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    And Validate the service record for expected "id" and "stateChange"
    And Validate the service record for expected "in_progressChange" state
    And Validate the service record for expected "mwr_id" value
    And I validate that a "MWR_service" record is found in "bi-controller-services" index
    And Validate that service "state" is "terminated"
    And Validate that service "in_progress" is "false"
    And I validate that a "request" record is found in "bi-controller-requests" index
    And I validate record format for "request" record
    And Validate that request "state" is "completed"
    And Validate that the "user_id" is same as the query parameter
    And Validate that a callback is sent to PubSub for "success"
    And Validate that the callback info has expected "correlationId" and status "success"
    Then I set BI "controller" url
    And I Set query parameters for controller request for "after"
    And Validate that the request id has deleted parameters
    And Validate the response has correct values against each key