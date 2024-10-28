@evpnController @cs
Feature: Patch Dry Run
  Patch an evpn service dry run request failure

  Scenario: This scenario validates failure from Mediation for a patch dry run request
    Given I read test data for CS testcases
    When Sending a patch-dry-run request
    Then Validating that evpn_bsaf_request_tracker record is updated with failed state
    And Validating that evpn_external_request_tracker record is updated with failed state
    Then Validating that callback is published in failed state in EVPN RMQ
    Then Validating that evpn_service record is-not created
    And Validating schema of failed callback published in EVPN

