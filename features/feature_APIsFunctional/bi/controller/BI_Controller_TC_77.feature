@controller @rmq
Feature: Validate controller response for delete service
  This features validates controller response for deleting a service successfully

  Scenario: Delete service successfully
    Given I set BI "controller" url
    And I set data values against test case "77"
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
    And Validate the service record for expected "in_progress" state
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I validate that a "service" record is found in "bi-controller-services" index
    And Validate the service record for expected "in_progressChange" state
    And I validate that a "request" record is found in "bi-controller-requests" index
    And Validate that request "state" is "completed"
    And Validate that the "user_id" is same as the query parameter
    And Validate that a callback is sent to PubSub for "success"
    And Validate that the callback info has expected "correlationId" and status "success"