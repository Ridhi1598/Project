@controller
Feature: Update elastic search data for service record
  This feature updates service record for in_progress state to true

   Scenario: Update service record for in_progress state to true
    Given I set data values against test case "53"
    And I read service id for test case
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And Update in_progress state for the service
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    When Validate the service record for "in-progress" state to be "true"