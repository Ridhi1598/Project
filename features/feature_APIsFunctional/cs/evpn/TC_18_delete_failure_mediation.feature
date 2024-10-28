Feature: Validate evpn response for delete service request
  This feature validates evpn response for delete service request fails at mediation


  Scenario: Delete Service request: failure response
    Given I read test data for CS testcases
    Then Sending a delete-service request
    Then Validating that evpn_bsaf_request_tracker record is updated with failed state
    And Validating that evpn_external_request_tracker record is updated with failed state
    And Validating that evpn_service record is created
    Then Validating that callback is published in failed state in EVPN RMQ
    And  Validating schema of failed callback published in EVPN
