@orchestrator @tc23 @updateService
Feature: Validate orchestrator response for executing update request  with multiple parameters origin from NC
  This features validates orchestrator response for executing update request with multiple parameters origin from NC

  Scenario: Update ES record for a create service in "bi-orchestrator-services" index
    Given I set data values against testcase
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "services" record
    And I set api request body for "create" a "services" record
    When I send HTTP request for "create" service
    Then I validate that the "services" record is "created" in "bi-orchestrator-services" index
    And I set api endpoint for "service" record for "read" ES message
    And I set request body for "service" record for "read" ES message
    And I validate that a "service" record is "created" in "bi-orchestrator-services" index
    And Validate the "original" values of "ipv4-lan-prefix" for "service" record
    And Validate the "original" values of "speed" for "service" record
    And Validate the "original" values of "port" for "service" record

  Scenario: Execute update request with multiple parameters origin from NC
    Given I set data values against testcase
    And I set BI "RMQ" url
    And I set api endpoint for "publish" message for "sending"
    And I set request body for "publish" message for "sending"
    And Send request to "publish" message in RMQ queue
    And Validate that response body has "routed" as "true"
    And I set api endpoint for "read" message for "sending"
    And I set request body for "read" message for "sending"
    And Send request to "read" message in RMQ queue
    And Validate that there is no message in the RMQ queue
    When I "start" zookeeper connectivity for node validation
    Then Validate a request id is returned by resource entity as synchronous response
    And I validate that a "node" is "created" in zookeeper instance
    And Wait for the callback response from "resource entity"
    And I validate that a "node" is "deleted" in zookeeper instance
    When I "stop" zookeeper connectivity for node validation
    And I set BI "ES" url
    And I set api endpoint for "request" record for "read" ES message
    And I set request body for "request" record for "read" ES message
    And I validate that a "request" record is "created" in "bi-orchestrator-requests" index
    And Validate a request id is returned by mediation layer as synchronous response
    And Wait for the callback response from "mediation layer"
    And I validate that a "request" record is "created" in "bi-orchestrator-requests" index
    And I validate record format for "request" response
    And Validate a callback response is returned by mediation layer as asynchronous response
    And Validate the "request_id" value in the response
    And Validate the "completed" value in the response
    And Validate the "state" value in the response
    And I set api endpoint for "service" record for "read" ES message
    And I set request body for "service" record for "read" ES message
    And I validate that a "service" record is "created" in "bi-orchestrator-services" index
    And I validate record format for "service" response
    And Validate that the service record has "the" same "associated-requests"
    And Validate that the service record has "vpn-id" in correct format
    And Validate the "modified" values of "ipv4-lan-prefix" for "service" record
    And The "original" and "modified" values of the "ipv4-lan-prefix" should be "different"
    And Validate the "modified" values of "speed" for "service" record
    And The "original" and "modified" values of the "speed" should be "different"
    And Validate the "modified" values of "port" for "service" record
    And The "original" and "modified" values of the "port" should be "different"
    And I set BI "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    And Send request to "read" message in RMQ queue
    And Validate that a "success" message is published to controller
    And Validate response format for "success" message
    And Validate that a "resources" section "is not present" in the callback response

  Scenario: Delete ES record for created service in "bi-orchestrator-services" index
    Given I set data values against testcase
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "services" record
    And I set api request body for "delete" a "services" record
    When I send HTTP request for "delete" service
    Then I validate that the "services" record is "deleted" in "bi-orchestrator-services" index