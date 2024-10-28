@ingestion
Feature: Validate ingestion response for display rollback config but request times out
  This features validates ingestion response for display rollback config but request times out

@displayRollbackConfig
  Scenario: Display rollback config but request times out
    Given I read test data for testcase
    Given I set "ingestion" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "ingestion" api endpoint
    And I Set "ingestion" api request body
    And I Set query parameters for "ingestion" request for "before"
    When I Send HTTP request for "ingestion"
    And I validate the response body should have "status" as "in-progress"
    And Wait for the expected timeout value for service
    And I Set query parameters for "ingestion" request for "after"
    When I Send HTTP request for "ingestion"
    And I validate the expected response schema
