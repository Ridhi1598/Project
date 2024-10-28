@controller
Feature: Validate controller response for executing a request originating from TINAA
  This features validates controller response for executing a request originating from TINAA

  Scenario: Executing an update request originating from TINAA
    Given I read test data for testcase
    When I generate access token for authorization
    And I Send "execute" request for "ingestion"
    When I "start" zookeeper connectivity for node validation
    And I validate that a "node" is "created" in zookeeper instance
    Then I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
    And I validate the service record for expected "before" "state" value
    And I validate the service record for expected "before" "in-progress" value
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "success" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate the service record for expected "after" "state" value
    And I validate the service record for expected "after" "in-progress" value
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And Validate that a callback is sent to PubSub for "success"
    And Validate that the callback info has expected "correlationId" and status "success"
    And Validate that request "state" is "completed"
    And Validate that request "source" is "TINAA"
    And I Set query parameters for "ingestion" request for "syncback"
    When I send request to "fetch" "syncback" record from "mock-server"
    And I Validate that the syncback response has expected transactionId
    And I validate that a "node" is "deleted" in zookeeper instance
    When I "stop" zookeeper connectivity for node validation

  Scenario: Delete callback responses from mock server records
    When I send request to "delete" "callback" record from "mock-server"
    Then I validate that the response has "status" as "deleted"


#  Scenario: Delete Temporary record
#    When I send request to "delete" a "BaseService" record in "ES" "request" record
#    When I send request to "delete" a "Service" record in "ES" "service" record
