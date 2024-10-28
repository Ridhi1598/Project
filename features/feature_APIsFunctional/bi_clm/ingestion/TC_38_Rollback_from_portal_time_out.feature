@ingestion
Feature: Validate ingestion response in case of modify service rollback timeout
  This features validates ingestion response in case of modify service rollback timeout

  Scenario: Modify service rollback: Timeout
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "rollback" request for "ingestion"
    And I extract response value for "requestId"
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And Validate that request "state" is "pending"
    And Execute the "rollback" request for processing
    When I "start" zookeeper connectivity for node validation
    And I validate that a "node" is "created" in zookeeper instance
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And I validate record format for "request" record
    And Validate that request "state" is "submitted"
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
    And I validate the service record for expected "before" "state" value
    And I validate the service record for expected "before" "in-progress" value
    Then Validate that the "request-tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Wait for the expected timeout value for service
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
    And I validate the service record for expected "after" "state" value
    And I validate the service record for expected "after" "in-progress" value
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And Validate that request "state" is "timeout"
    And Validate that the "user_id" is same as the query parameter
    And I validate that a "node" is "deleted" in zookeeper instance
    When I "stop" zookeeper connectivity for node validation

  Scenario: Delete callback responses from mock server records
    When I send request to "delete" "callback" record from "mock-server"
    Then I validate that the response has "status" as "deleted"

