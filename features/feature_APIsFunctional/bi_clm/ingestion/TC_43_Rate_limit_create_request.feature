@ingestion
Feature: Validate ingestion response for create service if concurrent requests count exceeds Rate Limit
  This features validates ingestion response for create service if concurrent requests count exceeds Rate Limit

  Scenario: Create service against Rate Limit
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "create" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response
