@IngestionEngine
Feature: Validate Ingestion engine response for L3VPN Service Status-false service
  This features validates Ingestion engine response for GET L3VPN Service Status-false service

  Scenario: GET status of non existing service
    Given I set L3VPN "IngestionEngine" url
    And I set data values against "testCase_23" for Ingestion Engine
    And I generate access token for L3VPN
    And I Set headers "Content" and "Authorization" for IE
    And I Set api endpoint and request Body for IE
    And I Set query parameters for Ingestion engine request
    When I Send HTTP request for IE
    And I validate the response schema for IE
    And I validate response body for expected "status" and "reason" for IE