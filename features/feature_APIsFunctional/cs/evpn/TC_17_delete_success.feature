
Feature: Validate evpn response for delete service request
  This features validates evpn response for successful delete service request

  Scenario: Delete Service request with success response
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
    And Validating that callback is published in completed state in EVPN RMQ
    Then Sending a create-commit request
    Then Fetching external_id from evpn_external_request_tracker
    Then Reading callback published from l2 in l2 topology RMQ
    And Publishing callback fetched from l2 topology queue to EVPN RMQ
    And Validating that evpn_service record is created
    Then Sending a delete-service request
    Then Fetching external_id from evpn_external_request_tracker
    Then Reading callback published from l2 in l2 topology RMQ
    And Publishing callback fetched from l2 topology queue to EVPN RMQ
    And Validating that evpn_service record is-not created
    And Validating that callback is published in completed state in EVPN RMQ
    And  Validating schema of success callback published in EVPN


  Scenario: Clean-up
    When Sending a delete-service soft-request
    Then Validating that evpn_service record is-not created
