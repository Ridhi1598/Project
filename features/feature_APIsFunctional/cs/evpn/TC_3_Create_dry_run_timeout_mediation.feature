@tc3 @evpnController @cs
Feature: Creat commit Dry Run
  Create an evpn service dry run request timeouts at mediation executor

  Scenario: This scenario validates timeout in creation of evpn dry run at mediation executor
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
    And Validating that evpn_external_request_tracker record is updated with in progress state
    Then Validating that callback is published in timeout state in EVPN RMQ
    And Validating that evpn_external_request_tracker record is updated with timeout state
    And Validating that evpn_bsaf_request_tracker record is updated with timeout state
    Then  Validating schema of timeout callback published in EVPN
