@ingestion @accessToken
Feature: Validate controller response for create service request
  This features validates controller response for create service request with missing token

  Scenario: Create service without Access Token
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "create" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response