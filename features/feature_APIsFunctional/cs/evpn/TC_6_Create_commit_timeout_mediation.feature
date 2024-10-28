@tc5 @evpnController @cs
Feature: Commit previous created evpn request using request-id
  Commit previous created evpn dry run request

  Scenario: This scenario validates timeout from mediation while for a commit request
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
    And Validating that callback is published in completed state in EVPN RMQ
    Then Sending a create-commit request
    And Validating that evpn_external_request_tracker record is updated with timeout state
    And Validating that evpn_bsaf_request_tracker record is updated with timeout state
    Then Validating that callback is published in timeout state in EVPN RMQ
    And  Validating schema of timeout callback published in EVPN
    And Validating that evpn_service record is-not created