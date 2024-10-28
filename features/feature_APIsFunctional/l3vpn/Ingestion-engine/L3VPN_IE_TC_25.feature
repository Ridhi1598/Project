@IngestionEngine @accessToken
Feature: Validate Monitor api response for Invalid request ID
  This features validates Monitor API response for Invalid request

  Scenario: With Invalid request ID
    Given I set L3VPN "IngestionEngine" url
    And I set data values against "testCase_25" for Ingestion Engine
    Then I generate access token for L3VPN
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    And I Set query parameters for Ingestion engine request
    When I Send HTTP request for IE
    And I validate the response schema for IE
    And I validate response body for expected result of failed Request