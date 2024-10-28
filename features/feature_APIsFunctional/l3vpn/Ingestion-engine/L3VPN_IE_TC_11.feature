@IngestionEngine
Feature: Validate controller response for modify service
  This features validates controller response for modifying a service with invalid payload

  Scenario: Modify an existing service with invalid payload

  Scenario: Create service with invalid payload
    Given I set L3VPN "IngestionEngine" url
    And I set data values against "testCase_11" for Ingestion Engine
    And I generate access token for L3VPN
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    And I Set query parameters for Ingestion engine request
    When I Send HTTP request for IE
    And I validate the response schema for IE
    And I validate response body for expected "status" and "reason" for IE