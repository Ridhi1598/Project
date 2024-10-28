Feature: Validate ingestion response for create service
  This features validates ingestion response for creating a successful service request through TINAA

  Scenario: Create GPON service through TINAA
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "create" request for "ingestion"
    And I extract response value for "requestId"
    And Execute the "create" request for processing
#    When I "start" zookeeper connectivity for node validation
#    And I validate that a "node" is "created" in zookeeper instance
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And Validate that request "state" is "submitted"
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
#    And I validate the service record for expected "before" "state" value
#    And I validate the service record for expected "before" "in-progress" value
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "in-process" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And Mock "success" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I validate that a "request" record is found in "clm-ingestion-service-services" index
    And Validate that request "state" is "completed"
    And I extract response value for service version
    And Validate that the "user_id" is same as the query parameter
#    And I Set query parameters for "ingestion" request for "callback"
#    When I send request to "fetch" "callback" record from "mock-server"
#    And Validate that the callback info has expected "correlationId" value
#    And Validate that the callback info has expected "status" value
    And I validate that a "service" record is found in "ingestion-services" index
#    And I validate record format for "service" record
    And I validate the service record for expected "after" "state" value
    And I validate the service record for expected "after" "in-progress" value
#    And I validate that a "node" is "deleted" in zookeeper instance
#    When I "stop" zookeeper connectivity for node validation

#  Scenario: Delete callback responses from mock server records
#    When I send request to "delete" "callback" record from "mock-server"
#    Then I validate that the response has "status" as "deleted"