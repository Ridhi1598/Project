@controller
Feature: Validate controller response in case of create service failure based on NSO Error
  This features validates controller response in case of create service failure due to nso error

  Scenario: Create service failure due to nso error: rollback-failed
    Given I set BI "controller" url
    And I set data values against test case "94"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set query parameters for controller request for "before"
    And I Set api endpoint and request Body
    When I Send HTTP request for controller
    And I validate the response schema
    And I extract response value for expected "requestId"
    And I validate that a "request" record is found in "bi-controller-requests" index
    And I validate record format for "request" record
    And Validate that request "state" is "submitted"
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    And Validate the service record for expected "id" and "state"
    And Validate the service record for expected "in_progress" state
    And Mock "nso-detailed-error" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I validate that a "request" record is found in "bi-controller-requests-test" index
    And Validate that request "state" is "failed"
    And Validate that the "user_id" is same as the query parameter
    And Validate that the "rollback-error-message" message is published to RMQ "tinaa-requests-tests" queue
    And Validate that a callback is sent to PubSub for "error"
    And Validate that the callback info has expected "correlationId" and status "error"
    And Validate that correct error code "ERR201" is published to NB
    And I validate that a "service" record is found in "bi-controller-services" index
    And Validate the service record for expected "in_progressChange" state