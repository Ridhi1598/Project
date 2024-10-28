@controller
Feature: Validate controller response with success message for rollback current and expected config for a rollback request
  This features validates controller response for rollback current and expected config for a rollback request

@rollback
  Scenario: Create service rollback success
    Given I set BI "controller" url
    And I set data values against test case "68"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I extract response value for expected "requestId"

@displayConfig
  Scenario: Display current and expected config for a rollback request: Failure
    Given I generate access token for authorization
    And I set BI "controller" url
    And I set data values against test case "111"
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate response body should have "status" as "in-progress"
    And Mock "display-current-config-failed" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And Mock "display-expected-config-failed" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I Set query parameters for controller request for "after"
    And I Send HTTP request for controller
    And I validate the response schema
    Then I validate response body should have "current-config" as expected response
    And I validate response body should have "expected-config" as expected response

  @cancel
  Scenario: Cancel a pending rollback request
    Given I set BI "controller" url
    And I set data values against test case "114"
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
    And Validate that request "source" is "TINAA"
    Given I set BI "controller" url
    And Validate that the request is "not" in "service queue"
    And Validate that the request is "found" in "dashboard"