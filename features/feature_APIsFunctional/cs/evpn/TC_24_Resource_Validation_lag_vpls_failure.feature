Feature: Validate mediation response for validate resource request
  Executor returns resource request response successfully but validation fails

  Scenario: Resource validation request with Lag and VPLS success response from Executor but validation fails
    Given I read test data for CS testcases
    Then Sending a validate-resource request
    Then Validating that evpn_bsaf_request_tracker record is created with failed state
    Then Validating that evpn_external_request_tracker record is created with completed state
    And Validating that callback is published in failed state in EVPN RMQ
    And Validating schema of rv-lag-vpls-failed callback published in EVPN
