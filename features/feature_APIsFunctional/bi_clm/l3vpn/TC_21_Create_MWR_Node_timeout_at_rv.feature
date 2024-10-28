Feature: Timeout in Create Node request with mwr params at resource validator
  This features tests timeout response of Create Node request with mwr params at resource validator
  Scenario: Timeout for Node creation request at resource validator
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
    Then Sending create-node payload with mwr param to L3VPN via RMQ
    Then Validating that request-record is in submitted state
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
#    And Validating that service-record in-progress is set to True
    Then Validating that callback is received for VALIDATE_RESOURCES in completed state
    And Validating that request-record is in timeout state
    Then Validating that error callback is published to orchestrator-response queue
    And  Validating schema of failed callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
