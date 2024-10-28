@IngestionEngine @accessToken
Feature: Validate Ingestion engine response for service request
  This features validates controller response for expired token

  Scenario: With Expired Access Token
    Given I set L3VPN "IngestionEngine" url
    And I set data values against "testCase_2" for Ingestion Engine
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    And I Set query parameters for Ingestion engine request
    When I Send HTTP request for IE
    And I validate the response schema for IE
    And I validate response body for expected result of "status" and "reason" for IE