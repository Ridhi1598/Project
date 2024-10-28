@tc1 @evpnController @cs
Feature: Creat commit Dry Run
  Create an evpn service dry run request successfully

  Scenario: This scenario validates create evpn dry run request
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
    Then Validating that evpn_bsaf_request_tracker record is updated with PENDING CONFIRMATION state
    And Validating that evpn_external_request_tracker record is updated with completed state
    Then Validating that callback is published in completed state in EVPN RMQ
    And  Validating schema of success callback published in EVPN

#
