Feature: Validate ingestion response for modify service
  This features validates ingestion response for modifying a service with invalid payload

  Scenario: Modify an existing service with invalid payload
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "update" request for "ingestion"
    And I validate the response body for expected "status" and "reason"
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
    And I validate the service record for expected "before" "state" value
    And I validate the service record for expected "before" "in-progress" value
