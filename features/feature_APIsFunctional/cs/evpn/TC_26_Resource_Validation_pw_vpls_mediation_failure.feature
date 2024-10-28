Feature: Validate mediation response for validate resource request
  This features validates mediation executor failure response for resource validation request

  Scenario: Resource validation request with PW and VPLS failure response from executor
    Given I read test data for CS testcases
    Then Sending a validate-resource request
    Then Validating that evpn_bsaf_request_tracker record is created with failed state
    Then Validating that evpn_external_request_tracker record is created with failed state
    And Validating that callback is published in failed state in EVPN RMQ
    And Validating schema of rv-pw-vpls-failed callback published in EVPN