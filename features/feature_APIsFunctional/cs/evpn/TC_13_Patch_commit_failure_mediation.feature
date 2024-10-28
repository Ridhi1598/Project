@evpnController @cs
Feature: Patch commit
  Patch commit request Failed

  Scenario: This scenario validates Failure response from mediation for a patch commit request
    Given I read test data for CS testcases
    When Sending a patch-dry-run request
    And Validating that callback is published in completed state in EVPN RMQ
    And Fetch interfaces list from table interface before sending patch request
    Then Sending a patch-commit request
    Then Validating that evpn_bsaf_request_tracker record is created with failed state
    And Validating that evpn_external_request_tracker record is updated with failed state
    Then Validating that callback is published in failed state in EVPN RMQ
    And Validating schema of failed callback published in EVPN
    And Validating that new interface is-not added
