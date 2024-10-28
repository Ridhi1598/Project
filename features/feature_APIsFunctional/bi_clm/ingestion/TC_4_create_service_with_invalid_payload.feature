@ingestion @createService @invalidPayload
Feature: Validate controller response for create service request
  This features validates controller response for create service with invalid payload

  Scenario: Create Service: Reject: Invalid Payload
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "create" request for "ingestion"
    Then I validate the response body for expected "status" and "reason"
    And I validate response should have "code" as expected response