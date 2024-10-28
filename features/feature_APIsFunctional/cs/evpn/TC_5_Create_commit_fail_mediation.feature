@tc5 @evpnController @cs
Feature: Commit previous created evpn request using request-id
  Commit previous created evpn dry run request

  Scenario: This scenario validates commit request getting failed at mediation
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
    And Validating that callback is published in completed state in EVPN RMQ
    Then Sending a create-commit request
    Then Validating that evpn_bsaf_request_tracker record is updated with failed state
    And Validating that evpn_external_request_tracker record is updated with failed state
    And Validating that callback is published in failed state in EVPN RMQ
    And Validating schema of success callback published in EVPN
    Then Validating that evpn_service record is-not created
