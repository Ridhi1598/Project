Feature: Validate ingestion response for delete service
  This features validates ingestion response for deleting a service in terminated state

  Scenario: Delete a service which is in terminated state
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "delete" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response
  And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate the service record for expected "before" "state" value
    And I validate the service record for expected "before" "in-progress" value
