@ingestion
Feature: Validate ingestion response for updating a request in pending state
  This features validates ingestion response for updating a request in pending state

@updateFromServiceQueue
  Scenario: Updating a pending service request
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "update" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response
    Then I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record