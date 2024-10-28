Feature: Validate ingestion response for delete service
  This features validates ingestion response for deleting a non existing service

  Scenario: Delete a non existing service
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "delete" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response