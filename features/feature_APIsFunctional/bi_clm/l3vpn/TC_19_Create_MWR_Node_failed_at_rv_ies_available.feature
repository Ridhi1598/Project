Feature: Create Node request with mwr params when IES is available on device
  This features tests success response of Create Node request with mwr params when IES is available on device
  Scenario: Create Node request with mwr params when IES is available on device
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
    Then Sending create-node payload with mwr param to L3VPN via RMQ
    Then Validating that request-record is in failed state
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
#    And Validating that service-record in-progress is set to True
    Then Validating that callback is received for VALIDATE_RESOURCES in completed state
    And Validating that callback response contains 'IES value is occupied' error message
    Then Validating that request-record state is failed
    Then Validating that error callback is published to orchestrator-response queue
    And  Validating schema of error callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
