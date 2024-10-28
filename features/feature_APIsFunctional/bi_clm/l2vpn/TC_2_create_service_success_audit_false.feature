Feature: Validate mediation response for validate resource request
  Executor returns resource request response successfully but validation fails

  Scenario: Resource validation request with PW,LAg and VPLS success response from Executor but validation fails
    Given I read test data for testcase
    Then Sending create-l2vpn-service to l2vpn controller
#    Then Validating that evpn_bsaf_request_tracker record is created with failed state
#    Then Validating that evpn_external_request_tracker record is created with completed state
#    And Validating that callback is published in failed state in EVPN RMQ
#    And Validating schema of rv-pw-lag-vpls-failed callback published in EVPN