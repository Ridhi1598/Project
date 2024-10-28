@IngestionEngine @invalidPayload
Feature: Validate Ingestion Engine response for create service
  This features validates controller response for creating a service with invalid payload

  Scenario: Create service with invalid payload
    Given I set L3VPN "IngestionEngine" url
    And I set data values against "testCase_4" for Ingestion Engine
    And I generate access token for L3VPN
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    And I Set query parameters for Ingestion engine request
    When I Send HTTP request for IE
    And I validate the response schema for IE
    And I validate response body for expected "status" and "reason" for IE