@orchestrator @tc100 @modifyService
Feature: Validate orchestrator response for updating base service for am MWR service from TINAA
  This features validates orchestrator response for updating base service for am MWR service from TINAA

  Background:
    Given I set data values against testcase

  Scenario: Update ES record for a create service record in "bi-orchestrator-services" index
    Given I set BI "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "services" record
    And I set api request body for "create" a "services" record for "2" operations
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
    And I set api endpoint for "create" a "requests" record for "createMwrService"
    And I set api request body for "create" a "requests" record for "createMwrService"
    When I send HTTP request for "create" service
    Then I validate that the "requests" record is "created" in "bi-orchestrator-requests" index for "createMwrService"

  Scenario: Updating base service for am MWR service from TINAA
    Given I set BI "ES" url
    And I set api endpoint for "service" record for "read" ES message
    And I set request body for "service" record for "read" ES message
    When I validate that a "service" record is "created" in "bi-orchestrator-services" index
    And Validate the "original" values of "provider-prefixes" for "service" record
    And Validate the "original" values of "customer-prefixes" for "service" record
    And Validate the "original" values of "port" for "service" record
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
    And Validate the "modified" values of "customer-prefixes" for "service" record
    And The "original" and "modified" values of the "customer-prefixes" should be "different"
    And Validate the "modified" values of "port" for "service" record
    And The "original" and "modified" values of the "port" should be "different"
    And Validate the "modified" values of "provider-prefixes" for "service" record
    And The "original" and "modified" values of the "provider-prefixes" should be "same"
    And I set BI "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    And Send request to "read" message in RMQ queue
    And Validate that a "success" message is published to controller
    And Validate response format for "success" message
    And Validate that a "resources" section "is present" in the callback response
    And Validate the "oldValue" and "newValue" for resources are present in the callback response
    And Validate that "port" values are "present" in the callback response
    And Validate that "customer-prefixes" values are "present" in the callback response
    And Validate that "provider-prefixes" values are "not present" in the callback response

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
    And I set api endpoint for "delete" a "requests" record for "createMwrService"
    And I set api request body for "delete" a "requests" record for "createMwrService"
    When I send HTTP request for "delete" service
    Then I validate that the "requests" record is "deleted" in "bi-orchestrator-requests" index for "createMwrService"