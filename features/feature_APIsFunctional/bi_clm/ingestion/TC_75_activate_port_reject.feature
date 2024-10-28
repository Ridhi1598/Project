Feature: Validate ingestion response for port activation
  This features validates ingestion response for port activation rejected request

  Scenario: Port activation for invalid service type - reject
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "activate" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response