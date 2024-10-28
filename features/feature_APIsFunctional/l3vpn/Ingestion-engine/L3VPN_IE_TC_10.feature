@ingestionEngine
Feature: Validate Ingestion engine response for modify service
  This features validates Ingestion engine response for modifying a service in terminated state

  Scenario: Modify a service in which is in terminated state
    Given I set L3VPN "IngestionEngine" url
    When I set data values against "testCase_10" for Ingestion Engine
    Then I generate access token for L3VPN
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    And I Set query parameters for Ingestion engine request
    When I Send HTTP request for IE
    Then I validate the response schema for IE
    And I validate response body for expected "status" and "reason" for IE