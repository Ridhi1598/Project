@orchestrator @tc159 @updateService
Feature: Validate orchestrator response for modify HS service request
  This features validates orchestrator response for failed modify service request due to unavailable port

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
    And Validate the "original" values of "port" for "service" record

  Scenario: Modify service by changing port but fails due to unavailable port: multiple errors
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
    Then I "stop" zookeeper connectivity for node validation
    When I set BI "ES" url
    And I set api endpoint for "request" record for "read" ES message
    And I set request body for "request" record for "read" ES message
    Then I validate that a "request" record is "not created" in "bi-orchestrator-requests" index
    And I set api endpoint for "service" record for "read" ES message
    And I set request body for "service" record for "read" ES message
    And I validate that a "service" record is "created" in "bi-orchestrator-services" index
    And Validate that the service record has no record of "associated-requests"
    And Validate the "modified" values of "port" for "service" record
    And The "original" and "modified" values of the "port" should be "same"
    When I set BI "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    Then Send request to "read" message in RMQ queue
    But Validate that a "error" message is published to controller
    And Validate response format for "failed" message
    And Validate that the error "message" in callback is correctly mapped
    And Validate that the error "code" in callback is correctly mapped

  Scenario: Delete ES record for created service in "bi-orchestrator-services" index
    Given I set data values against testcase
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "services" record
    And I set api request body for "delete" a "services" record
    When I send HTTP request for "delete" service
    Then I validate that the "services" record is "deleted" in "bi-orchestrator-services" index