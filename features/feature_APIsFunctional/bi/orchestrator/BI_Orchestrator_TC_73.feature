@orchestrator @tc73 @rollbackService
Feature: Validate orchestrator response for rolling back a delete request
  This features validates orchestrator response for rolling back a delete request

  Background:
    Given I set data values against testcase

  Scenario: Update ES record for a create service record in "bi-orchestrator-services" index
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "services" record
    And I set api request body for "create" a "services" record for "1" operations

  Scenario: Update ES record for a create request record in "bi-orchestrator-requests" index
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "requests" record for "deleteService"
    And I set api request body for "create" a "requests" record for "deleteService"
    When I send HTTP request for "create" service
    Then I validate that the "requests" record is "created" in "bi-orchestrator-requests" index for "deleteService"

  Scenario: Rollback a delete request
    Given I set data values against testcase
    And I set BI "RMQ" url
    And I set api endpoint for "publish" message for "sending"
    And I set request body for "publish" message for "rollback"
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
    And Validate that the "error" message in callback is as expected

  Scenario: Delete ES record for created request in "bi-orchestrator-requests" index
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "requests" record for "deleteService"
    And I set api request body for "delete" a "requests" record for "deleteService"
    When I send HTTP request for "delete" service
    Then I validate that the "requests" record is "deleted" in "bi-orchestrator-requests" index for "deleteService"