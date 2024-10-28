@tc2 @evpnController @cs
Feature: Creat commit Dry Run
  Create an evpn service dry run request fails at mediation executor

  Scenario: This scenario validates failure in creation of evpn dry run on mediation executor
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
#    Then Publishing payload to RMQ
    Then Validating that evpn_bsaf_request_tracker record is updated with failed state
    And Validating that evpn_external_request_tracker record is updated with failed state
    Then Validating that callback is published in failed state in EVPN RMQ
    And  Validating schema of failed callback published in EVPN
