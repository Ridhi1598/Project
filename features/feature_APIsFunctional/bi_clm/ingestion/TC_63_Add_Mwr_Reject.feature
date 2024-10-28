@ingestion @mwr
Feature: Validate ingestion response for Add Mwr Request
  This features validates ingestion response for rejected Mwr Request

  Scenario: Add Mwr Reject
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "add-mwr" request for "ingestion"
    And I validate the response body for expected "status" and "reason"
    And I validate response should have "code" as expected response