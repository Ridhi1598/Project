@ingestion
Feature: Validate ingestion response for executing a request in invalid state
  This features validates ingestion response for executing a request in invalid state

@update
  Scenario: Executing an update request in invalid state
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "execute" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response
    Then I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And Validate that request "state" is not "pending"
