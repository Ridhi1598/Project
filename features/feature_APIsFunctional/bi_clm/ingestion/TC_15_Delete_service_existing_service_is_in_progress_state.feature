Feature: Validate ingestion response for delete service
  This features validates ingestion response for deleting a service in progress state


Scenario: Update service record for in_progress state to true
    Given I set data values against test case "53"
    And I read service id for test case
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And Update in_progress state for the service
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    When Validate the service record for "in-progress" state to be "true"


  Scenario: Delete a service which is in progress state
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "delete" request for "ingestion"
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response
  Then I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
    And I validate the service record for expected "before" "state" value
    And I validate the service record for expected "before" "in-progress" value
    And Validate the service record for "in-progress" state to be "true"


   Scenario: Update service record for in_progress state to false
    Given I set data values against test case "54"
    And I set BI "ES" url
    And I read service id for test case
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    When Validate the service record for "in-progress" state to be "true"
    And Update in_progress state for the service
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    When Validate the service record for "in-progress" state to be "false"