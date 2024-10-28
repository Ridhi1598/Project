Feature: Validate ingestion response for create service request
  This features validates ingestion response for create service request with expired token

  Scenario: Create Service With Expired Access Token
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "create" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
