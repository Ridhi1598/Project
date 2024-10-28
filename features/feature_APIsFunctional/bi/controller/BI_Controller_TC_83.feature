@controller
Feature: Validate controller response for execute request if concurrent requests count exceeds Rate Limit
  This features validates controller response for execute request if concurrent requests count exceeds Rate Limit

  Scenario: Execute update request against Rate Limit
    Given I set BI "controller" url
    And I set data values against test case "83"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body for expected "status" and "reason"

  Scenario: Update ES record for a delete request record in "bi-controller-requests" index
    Given I set BI "ES" url
    And I set data values against test case "103"
    And I create a document id for request record creation
    And I set api endpoint for "delete" a requests record
    And I set api request body for "delete" a requests record
    When I send HTTP request for "delete" service
    Then I validate that the requests record is "deleted"

  Scenario: Execute update request against Rate Limit
    Given I set BI "controller" url
    And I set data values against test case "83"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    When I Send HTTP request for controller
    And I validate response body should have "status" as "success"
    And I validate that a "request" record is found in "bi-controller-requests" index
    And Validate that request "state" is "submitted"
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And I validate that a "request" record is found in "bi-controller-requests" index
    And Validate that request "state" is "completed"