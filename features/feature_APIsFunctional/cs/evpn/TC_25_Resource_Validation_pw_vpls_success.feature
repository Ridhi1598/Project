Feature: Validate mediation response for validate resource request
  This features validates mediation executor response for successful resource validation request

  Scenario: Resource validation request with PW and VPLS success response
    Given I read test data for CS testcases
    Then Sending a validate-resource request
    Then Validating that evpn_bsaf_request_tracker record is created with completed state
    Then Validating that evpn_external_request_tracker record is created with completed state
    And Validating that callback is published in completed state in EVPN RMQ
    And Validating schema of success callback published in EVPN
