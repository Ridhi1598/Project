@ingestion
Feature: Validate ingestion response in case of create service rollback failure
  This features validates ingestion response for create service rollback failure message

@Rollback
  Scenario: Create service rollback failure message
    Given I read test data for testcase
    Given I set "ingestion" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "ingestion" api endpoint
    And I Set "ingestion" api request body
    And I Set query parameters for "ingestion" request for "before"
    When I Send HTTP request for "ingestion"
