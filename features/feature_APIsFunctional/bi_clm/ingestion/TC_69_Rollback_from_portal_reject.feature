@ingestion
Feature: Validate ingestion response in case of modify service rollback success
  This features validates ingestion response in case of modify service rollback success


  Scenario: Modify service rollback
 Given I read test data for testcase
    And I generate access token for authorization
    When I Send "rollback" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response