@ingestion @mwr
Feature: Validate ingestion response for Delete Mwr Request
  This features validates ingestion response for rejected Mwr Request

  Scenario: Delete Mwr Reject
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "delete-mwr" request for "ingestion"
    And I validate the response body for expected "status" and "reason"
    And I validate response should have "code" as expected response