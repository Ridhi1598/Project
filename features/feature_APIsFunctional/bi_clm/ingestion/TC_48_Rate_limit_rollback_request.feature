@ingestion
Feature: Validate ingestion response for Rollback service if concurrent requests count exceeds Rate Limit
  This features validates ingestion response for Rollback service if concurrent requests count exceeds Rate Limit


  Scenario: Rollback service against Rate Limit
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "delete" request for "ingestion"
    And I extract response value for "requestId"
    And Execute the "rollback" request for processing
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response