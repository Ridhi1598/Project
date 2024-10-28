@ingestion
Feature: Validate ingestion response for display rollback config with success message
  This features validates controller response for display rollback config with success message

@displayRollbackConfig
  Scenario: Display rollback config with success message
    Given I read test data for testcase
    Given I set "ingestion" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "ingestion" api endpoint
    And I Set "ingestion" api request body
    And I Set query parameters for "ingestion" request for "before"
    When I Send HTTP request for "ingestion"
    And I validate the response body should have "status" as "in-progress"
    And Mock "display-config-success" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I Set query parameters for "ingestion" request for "after"
    When I Send HTTP request for "ingestion"
    And I validate the expected response schema