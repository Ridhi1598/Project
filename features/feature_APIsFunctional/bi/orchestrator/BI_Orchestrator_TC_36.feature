@orchestrator @tc36 @displayRollbackConfig
Feature: Validate orchestrator response for executing display rollback config request
  This features validates orchestrator response for executing display rollback config request

  Background:
    Given I set data values against testcase

  Scenario: Update ES record for a create service record in "bi-orchestrator-services" index
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "services" record
    And I set api request body for "create" a "services" record for "3" operations
    When I send HTTP request for "create" service
    Then I validate that the "services" record is "created" in "bi-orchestrator-services" index for "service"

  Scenario: Update ES record for a create request record in "bi-orchestrator-requests" index
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "requests" record for "baseService"
    And I set api request body for "create" a "requests" record for "baseService"
    When I send HTTP request for "create" service
    Then I validate that the "requests" record is "created" in "bi-orchestrator-requests" index for "baseService"

  Scenario: Update ES record for a create request record in "bi-orchestrator-requests" index
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "requests" record for "modifyBaseService"
    And I set api request body for "create" a "requests" record for "modifyBaseService"
    When I send HTTP request for "create" service
    Then I validate that the "requests" record is "created" in "bi-orchestrator-requests" index for "modifyBaseService"

  Scenario: Update ES record for a create request record in "bi-orchestrator-requests" index
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "requests" record for "rollbackService"
    And I set api request body for "create" a "requests" record for "rollbackService"
    When I send HTTP request for "create" service
    Then I validate that the "requests" record is "created" in "bi-orchestrator-requests" index for "rollbackService"

  Scenario: Failed display rollback config request
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
    And Validate a request id is returned by mock server for display rollback config
    And Wait for the callback response from "mediation layer"
    And I validate that a "displayRequest" record is "created" in "bi-orchestrator-requests" index
    And I validate record format for "request" response
    And Validate a callback response is returned by mock server for display rollback config
    And Validate the "request_id" value in the response
    And Validate the "completed" value in the response
    And Validate the "state" value in the response
    And Validate that "audit" field is not present in the response
    And I set BI "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    And Send request to "read" message in RMQ queue
    And Validate that a "error" message is published to controller
    And Validate response format for "failed" message
    And Validate that a "display_config_payload" section "is present" in the callback response

  Scenario: Delete ES record for created service in "bi-orchestrator-services" index
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "services" record
    And I set api request body for "delete" a "services" record
    When I send HTTP request for "delete" service
    Then I validate that the "services" record is "deleted" in "bi-orchestrator-services" index for "service"

  Scenario: Delete ES record for created request in "bi-orchestrator-requests" index
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "requests" record for "baseService"
    And I set api request body for "delete" a "requests" record for "baseService"
    When I send HTTP request for "delete" service
    Then I validate that the "requests" record is "deleted" in "bi-orchestrator-requests" index for "baseService"

  Scenario: Delete ES record for created request in "bi-orchestrator-requests" index
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "requests" record for "modifyBaseService"
    And I set api request body for "delete" a "requests" record for "modifyBaseService"
    When I send HTTP request for "delete" service
    Then I validate that the "requests" record is "deleted" in "bi-orchestrator-requests" index for "modifyBaseService"

  Scenario: Delete ES record for created request in "bi-orchestrator-requests" index
    Given I set BI "ES" url
    And I set api endpoint for "delete" a "requests" record for "rollbackService"
    And I set api request body for "delete" a "requests" record for "rollbackService"
    When I send HTTP request for "delete" service
    Then I validate that the "requests" record is "deleted" in "bi-orchestrator-requests" index for "rollbackService"