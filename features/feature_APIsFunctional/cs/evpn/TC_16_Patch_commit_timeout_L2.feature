@evpnController @cs
Feature: Patch commit
  Patch commit request timeout at L2


  Scenario: This scenario validates a Timeout response from EVPN for L2 patch commit request
    Given I read test data for CS testcases
    When Sending a create-dry-run request
    Then Validating that callback is published in completed state in EVPN RMQ
    And Sending a create-commit request
    Then Fetching external_id from evpn_external_request_tracker
    Then Reading callback published from l2 in l2 topology RMQ
    And Publishing success callback fetched from l2 topology queue to EVPN RMQ
    And Validating that evpn_service record is created
    When Sending a patch-dry-run request
    Then Validating that callback is published in completed state in EVPN RMQ
    Then Sending a patch-commit request
    Then Validating that evpn_external_request_tracker record is updated with completed state
    Then Validating that evpn_external_request_tracker record is updated with in progress state
    Then Validating that evpn_bsaf_request_tracker record is updated with completed state
    And Validating that callback is published in completed state in EVPN RMQ
    And  Validating schema of success callback published in EVPN
    And Validating that new interface is-not added

  Scenario: Clean-up
    When Sending a delete-service request
    Then Validating that evpn_service record is-not created
    And Validating that callback is published in completed state in EVPN RMQ
