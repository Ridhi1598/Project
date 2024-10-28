@orchestrator @tc147 @createService
Feature: Validate orchestrator response for create GPON-QINQ service request
  This features validates orchestrator response for failed create service request due to non existent lag

  Scenario: Create GPON-QinQ Service which fails: Non Existent lag
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
    When I set BI "ES" url
    And I set api endpoint for "request" record for "read" ES message
    And I set request body for "request" record for "read" ES message
    Then I validate that a "request" record is "not created" in "bi-orchestrator-requests" index
    When I set api endpoint for "service" record for "read" ES message
    And I set request body for "service" record for "read" ES message
    Then I validate that a "service" record is "not created" in "bi-orchestrator-services" index
    When I set BI "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    Then Send request to "read" message in RMQ queue
    But Validate that a "error" message is published to controller
    And Validate response format for "failed" message
    And Validate that the error "code" in callback is correctly mapped