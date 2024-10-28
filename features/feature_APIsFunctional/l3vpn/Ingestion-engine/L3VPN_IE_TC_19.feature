@IngestionEngine
Feature: Validate Ingestion engine response for delete service
  This features validates Ingestion engine response for deleting a service but request times out

  Scenario: Delete service but the request times out
    Given I set L3VPN "IngestionEngine" url
    When I set data values against "testCase_19" for Ingestion Engine
    Then I generate access token for L3VPN
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    And I get the Webhook instance for validating callback responses
    And I Set query parameters for Ingestion engine request
    When I Send HTTP request for IE
    Then I validate the response schema for IE
    Then I extract "requestId" from the expected response
    And I validate that a "request" record is found in "l3vpn-ingestion-engine-requests" index for IE
	And I validate "request" record format
    And I validate that the request "state" is "submitted"
    And I validate that a "service" record is found in "l3vpn-ingestion-engine-services" index for IE
    And I validate "service" record format
    And I validate the service record for expected "id" and "state"
    And I validate the service record for expected "in_progress" state
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue for IE
	And I Wait for the expected timeout value for service
    And I validate that a "request" record is found in "tinaa-requests-tests" index for IE
    And I validate that the request "state" is "timeout"
    And I validate that the callback response is sent for "timeout"
    And Validate that callback info has expected "correlationId" and status "timeout"