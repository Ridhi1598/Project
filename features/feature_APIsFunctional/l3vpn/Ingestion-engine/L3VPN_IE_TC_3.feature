@IngestionEngine
Feature: Validate Ingestion engine response for create service
  This features validates Ingestion engine response for creating a failed service request

  Scenario: Create service with valid payload and service but fails
    Given I set L3VPN "IngestionEngine" url
    When I set data values against "testCase_6" for Ingestion Engine
    Then I generate access token for L3VPN
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    And I get the Webhook instance for validating callback responses
    And I Set query parameters for Ingestion engine request
    When I Send HTTP request for IE
    Then I validate the response schema for IE
    Then I extract "requestId" from the expected response


  Scenario: Create service with valid payload and service state is in in-progress state
    Given I set L3VPN "IngestionEngine" url
    When I set data values against "testCase_3" for Ingestion Engine
    Then I generate access token for L3VPN
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    When I Send HTTP request for IE
    Then I validate the response schema for IE
    And I validate response body for expected "status" and "reason" for IE


 Scenario: Mock success response for failed callback
   Given I set data values against "testCase_6" for Ingestion Engine
   When Mock "error" response to be published to RMQ "tinaa-l3vpn-request-callbacks" queue for IE
   Then I validate that a "service" record is found in "l3vpn-ingestion-engine-services" index for IE
   And I validate "service" record format
   And I validate the service record "found" value should be "false"