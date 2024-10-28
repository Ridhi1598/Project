@ingestion
Feature: Validate ingestion response for portal display service parameters
  This features validates ingestion response for display service parameters based on the service version

@portalCall
  Scenario: Validate ingestion response for display service parameters
    Given I read test data for testcase
    Given I set "ingestion" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "ingestion" api endpoint
    And I Set "ingestion" api request body
    And I Set query parameters for "ingestion" request for "before"
    When I Send HTTP request for "ingestion"
    And I validate the expected response schema
