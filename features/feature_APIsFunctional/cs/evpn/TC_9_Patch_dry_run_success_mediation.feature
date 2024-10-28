@evpnController @cs
Feature: Patch Dry Run
  Patch an evpn service dry run request successfully

  Scenario: This scenario validates patch dry run request
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
    Then Validating that callback is published in completed state in EVPN RMQ
    Then Sending a create-commit request
    Then Fetching external_id from evpn_external_request_tracker
    Then Reading callback published from l2 in l2 topology RMQ
    And Publishing callback fetched from l2 topology queue to EVPN RMQ
    And Validating that evpn_service record is created
    Then Sending a patch-dry-run request
    And Validating that evpn_bsaf_request_tracker record is created with PENDING CONFIRMATION state
    And Validating that evpn_external_request_tracker record is updated with completed state
    Then Validating that callback is published in completed state in EVPN RMQ
    And Validating schema of success callback published in EVPN


  Scenario: Clean-up
    Given I read test data for CS testcases
    When Sending a delete-service request
    Then Validating that evpn_service record is-not created
    And Validating that callback is published in completed state in EVPN RMQ

