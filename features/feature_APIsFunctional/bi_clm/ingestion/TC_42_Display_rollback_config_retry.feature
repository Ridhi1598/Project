@ingestion
Feature: Validate ingestion response for display rollback config for retry scenario
  This features validates ingestion response for display rollback config for retry scenario

@displayRollbackConfig
  Scenario: Display before and after rollback config for retry scenario
    Given I read test data for testcase
    Given I set "ingestion" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "ingestion" api endpoint
    And I Set "ingestion" api request body
    And I Set query parameters for "ingestion" request for "before"
    When I Send HTTP request for "ingestion"
    And I validate the response body should have "status" as "in-progress"
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "display-config-failed" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I Set query parameters for "ingestion" request for "after"
    When I Send HTTP request for "ingestion"
    Then I validate the response body should have "status" as "error"