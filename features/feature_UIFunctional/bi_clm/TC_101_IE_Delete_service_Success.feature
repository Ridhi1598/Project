@tc101
Feature: Validate ingestion response for delete service
  This features validates ingestion response for deleting a service successfully

  Scenario: Delete service successfully
    Given I read test data for testcase
    When I set "ingestion" url
    Then I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "ingestion" api endpoint
    And I Set "ingestion" api request body
    And I Set query parameters for "ingestion" request for "before"
    When I Send HTTP request for "ingestion"
    And I extract response value for "requestId"
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And Validate that request "state" is "submitted"
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And Validate the service record for expected "id" and "state_before"
    And Validate the service record for expected "in-progress_before" state
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "in-process" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And Mock "success" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I validate that a "request" record is found in "clm-ingestion-service-services" index
    And Validate that request "state" is "completed"
    And Validate that the "user_id" is same as the query parameter
    And I Set query parameters for "ingestion" request for "callback"
    When I send request to "fetch" "callback" record from "mock-server"
    Then I validate the "callback" response format for "success" message
    And Validate that the callback info has expected "correlationId" value
    And Validate that the callback info has expected "status" value
    And I validate that a "service" record is found in "ingestion-services" index
    And Validate the service record for expected "in-progress_after" state


  Scenario: Delete callback responses from mock server records
    When I send request to "delete" "callback" record from "mock-server"
    Then I validate that the response has "status" as "deleted"


