@controller
Feature: Validate controller response in case of modify service rollback success
  This features validates controller response in case of modify service rollback success

  Scenario: Modify service rollback success: Success
    Given I set BI "controller" url
    And I set data values against test case "68"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I extract response value for expected "requestId"
    And I validate that a "request" record is found in "bi-controller-requests" index
    And Validate that request "state" is "pending"
    And Execute the update request for processing
    And I validate that a "request" record is found in "bi-controller-requests" index
    And I validate record format for "request" record
    And Validate that request "state" is "submitted"
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    And Validate the service record for expected "id" and "state"
    And Validate the service record for expected "in_progress" state
    Then Validate that the "rollback-portal" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "rollback-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    And Validate the service record for expected "id" and "stateChange"
    And Validate the service record for expected "in_progressChange" state
    And I validate that a "request" record is found in "bi-controller-requests" index
    And Validate that request "state" is "completed"
    And Validate that the "user_id" is same as the query parameter
    And Validate that a callback is sent to PubSub for "successRollback"
    And Validate that the callback info has expected "correlationId" and status "success"
    And Validate that "@rollbackBaseService" field is "present" in callback info
    And Validate that the callback info has "@rollbackBaseService" set as "Yes"
    And Validate that the callback info has "Value" as "serviceId"
    And Validate that "@rollbackMWRService" field is "not present" in callback info