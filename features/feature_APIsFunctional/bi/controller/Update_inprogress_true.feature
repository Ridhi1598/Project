@controller
Feature: Update elastic search data for service record
  This feature updates service record for in_progress state to true

  Scenario: Update service record for in_progress state to true
    Given I set data values against test case "37"
    And I read service id for test case
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    When Validate the service record for "in_progress" state to be "false"
    And Update in_progress state for the service
    Then Validate that service record "result" is "updated"
    And I validate that a "service" record is found in "bi-controller-services" index
    And I validate record format for "service" record
    When Validate the service record for "in_progress" state to be "true"