@ingestion
Feature: Validate ingestion response for display before and after config for an update request
  This features validates ingestion response for display before and after config for an update request

@displayConfig
  Scenario: Display before and after config for retry scenario
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "display" request for "ingestion"
    And I validate the response body should have "status" as "in-progress"
    Then Validate that the "request tracker" message is published to RMQ "tinaa-requests-tests" queue
    And Mock "display-config-failed" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I Set query parameters for "ingestion" request for "after"
    When I Send HTTP request for "ingestion"
    Then I validate the response body should have "status" as "error"