@orchestrator @tc93 @rateLimit
Feature: Validate orchestrator response for add mwr with more than 3 requests in progress state
  This features validates orchestrator response for add mwr with more than 3 requests in progress state

  Scenario: Update ES record for a create service in "bi-orchestrator-services" index
    Given I set data values against testcase
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "services" record
    And I set api request body for "create" a "services" record
    When I send HTTP request for "create" service
    Then I validate that the "services" record is "created" in "bi-orchestrator-services" index

  Scenario: Add Mwr with 3 requests in progress
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
    And I set BI "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    And Send request to "read" message in RMQ queue
    And Validate that a "error" message is published to controller
    And Validate response format for "failed" message
    And Validate that the error "code" in callback is correctly mapped
    And Validate that the "error" message in callback is as expected

  Scenario: Delete ES record for created service in "bi-orchestrator-services" index
    Given I set data values against testcase
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "services" record
    And I set api request body for "delete" a "services" record
    When I send HTTP request for "delete" service
    Then I validate that the "services" record is "deleted" in "bi-orchestrator-services" index