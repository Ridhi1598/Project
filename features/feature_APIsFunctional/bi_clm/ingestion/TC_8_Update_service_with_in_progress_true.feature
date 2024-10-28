Feature: Validate ingestion response for modify service
  This features validates ingestion response for modifying a service in progress state

  Scenario: Update service record for in_progress state to true
    Given I set data values against test case "53"
    And I read service id for test case
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And Update in_progress state for the service
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    When Validate the service record for "in-progress" state to be "true"

  Scenario: Modify a service which is in progress state
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "update" request for "ingestion"
    And I validate the response body for expected "status" and "reason"
    And I validate that a "service" record is found in "clm-ingestion-service-services" index

   Scenario: Update service record for in_progress state to false
    Given I set data values against test case "54"
    And I set BI "ES" url
    And I read service id for test case
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    When Validate the service record for "in-progress" state to be "true"
    And Update in_progress state for the service
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    When Validate the service record for "in-progress" state to be "false"