@orchestrator @tc26 @displayConfig
Feature: Validate orchestrator response for failed display config request
  This features validates orchestrator response for failed display config request

  Scenario: Update ES record for a create service in "bi-orchestrator-services" index
    Given I set data values against testcase
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "services" record
    And I set api request body for "create" a "services" record
    When I send HTTP request for "create" service
    Then I validate that the "services" record is "created" in "bi-orchestrator-services" index

  Scenario: Failed display config request for Modify
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
    And I set BI "ES" url
    And I set api endpoint for "request" record for "read" ES message
    And I set request body for "displayRequest" record for "read" ES message
    And I validate that a "displayRequest" record is "created" in "bi-orchestrator-requests" index
    And Validate that "2" request ids are returned by mediation layer
    And Validate a request id is returned for "current" config
    And Validate a request id is returned for "expected" config
    And Wait for the callback response from "mediation layer"
    And I validate that a "displayRequest" record is "created" in "bi-orchestrator-requests" index
    And I validate record format for "request" response for "displayRequest"
    And Validate a callback response is returned by mock server for "current" config
    And Validate the "request_id" value in the response for "current" config
    And Validate the "completed" value in the response for "current" config
    And Validate the "state" value in the response for "current" config
    And Validate that "audit" field is not present in the response for "current" config
    And Validate a callback response is returned by mock server for "expected" config
    And Validate the "request_id" value in the response for "expected" config
    And Validate the "completed" value in the response for "expected" config
    And Validate the "state" value in the response for "expected" config
    And Validate that "audit" field is not present in the response for "expected" config
    And I set BI "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    And Send request to "read" message in RMQ queue
    And Extract current and expected config messages
    And I validate the "error" response and format for "current" config
    And I validate the "error" response and format for "expected" config

  Scenario: Delete ES record for created service in "bi-orchestrator-services" index
    Given I set data values against testcase
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "services" record
    And I set api request body for "delete" a "services" record
    When I send HTTP request for "delete" service
    Then I validate that the "services" record is "deleted" in "bi-orchestrator-services" index