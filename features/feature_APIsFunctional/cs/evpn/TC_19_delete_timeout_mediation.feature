Feature: Validate evpn response for delete service request
  This features validates evpn response for successful delete service request

  Scenario: Delete Service request with success response
    Given I read test data for CS testcases
    Then Sending a delete-service request
    And Validating that evpn_external_request_tracker record is updated with in progress state
    Then Validating that evpn_service record is created
    Then Validating that callback is published in timeout state in EVPN RMQ
    And  Validating schema of timeout callback published in EVPN



