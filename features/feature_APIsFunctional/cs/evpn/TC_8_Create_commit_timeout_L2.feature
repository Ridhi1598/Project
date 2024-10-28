@tc5 @evpnController @cs
Feature: Commit previous created evpn request using request-id
  Commit previous created evpn dry run request

  Scenario: This scenario validates EVPN functionality after commit request timeouts at L2
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
    And Validating that callback is published in completed state in EVPN RMQ
    Then Sending a create-commit request
    Then Validating that evpn_external_request_tracker record is updated with in progress state
    Then Validating that evpn_bsaf_request_tracker record is updated with completed state
    And Validating that callback is published in completed state in EVPN RMQ
    And Validating that evpn_service record is-not created
    And Validating schema of success callback published in EVPN

  Scenario: Clean-up
    When Sending a delete-service request
    Then Validating that evpn_service record is-not created
    And Validating that callback is published in completed state in EVPN RMQ
