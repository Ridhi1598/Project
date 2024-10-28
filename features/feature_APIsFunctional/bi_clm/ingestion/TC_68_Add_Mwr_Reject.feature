@ingestion @mwr
Feature: Validate ingestion response for Add Mwr Request
  This features validates ingestion response for rejected Mwr Request

  Scenario: Add Mwr Reject
    Given I read test data for testcase
    When I create "1" document id for request record creation
    When I send request to "create" a "BaseService" record in "ES" "request" record
    And I send request to "create" a "Service" record in "ES" "service" record

    Then I generate access token for authorization
    When I Send "add-mwr" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response

  Scenario: Delete temporary records
    When I send request to "delete" a "BaseService" record in "ES" "request" record
    And I send request to "delete" a "Service" record in "ES" "service" record