@evpnController @cs
Feature: Patch Dry Run
  Patch an evpn service dry run request timeout

  Scenario: This scenario validates timeout from Mediation for a patch dry run request
    Given I read test data for CS testcases
    When Sending a patch-dry-run request
    And Validating that evpn_external_request_tracker record is updated with in progress state
    Then Validating that callback is published in timeout state in EVPN RMQ
    And Validating that evpn_external_request_tracker record is updated with timeout state
    And Validating that evpn_bsaf_request_tracker record is updated with timeout state
    Then Validating that evpn_service record is-not created
    And Validating schema of timeout callback published in EVPN

