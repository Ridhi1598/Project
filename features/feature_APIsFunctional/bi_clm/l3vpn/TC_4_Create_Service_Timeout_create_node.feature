Feature: Validate l3vpn controller response for create service request
  This features validates l3vpn controller response for the timeout at CREATE_NODE.NODE

  Scenario: Create Service request with CREATE_NODE.NODE timeout response from l3vpn controller
    Given I read test data for testcase
    When Validating that service-record is not created in ES
    Then Sending create-service payload to L3VPN via RMQ
    Then Validating that request-record is in submitted state
    And Validating that in-process callback is published to orchestrator-response queue
    Then Validating schema of in-process callback published in orchestrator
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to True
    Then Validating that callback is received for VALIDATE_RESOURCES in completed state
    And Validating that callback is received for CREATE_PROFILES in completed state
    And Validating that request-record is in timeout state
    Then Validating that error callback is published to orchestrator-response queue
    And  Validating schema of failed callback published in orchestrator
    Then Validating that callback is received for TIMEOUT in in-progress state
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
