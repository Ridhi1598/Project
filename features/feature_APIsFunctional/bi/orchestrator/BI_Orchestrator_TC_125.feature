@orchestrator @tc125 @updateService
Feature: Validate orchestrator response for modify HS service request
  This features validates orchestrator response for modifying a non existent HS service

  Scenario: Modify an HS service but fails since service does not exists
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
    And Wait for the callback response from "mediation layer"
    And I set BI "ES" url
    And I set api endpoint for "service" record for "read" ES message
    And I set request body for "service" record for "read" ES message
    And I validate that a "service" record is "not created" in "bi-orchestrator-services" index
    And I set BI "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    And Send request to "read" message in RMQ queue
    And Validate that a "error" message is published to controller
    And Validate response format for "failed" message
    And Validate that the error "code" in callback is correctly mapped