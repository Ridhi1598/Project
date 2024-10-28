Feature: Validate l3vpn controller response for create service request
  This features validates l3vpn controller response from l3vpn controller for Resource validation

  Scenario: Create Service request with failure response from l3vpn controller for Resource validation
    Given I read test data for testcase
    When Validating that service-record is not created in ES
    Then Sending create-service payload to L3VPN via RMQ
    Then Validating that request-record is in failed state
    And Validating that in-process callback is published to orchestrator-response queue
    Then Validating schema of in-process callback published in orchestrator
    Then Validating that service-record is created in ES
    Then Validating that callback is received for VALIDATE_RESOURCES in completed state
    And Validating that callback response contains 'IES value is occupied' error message
    Then Validating that request-record state is failed
    And Validating that service-record is deleted
    Then Validating that error callback is published to orchestrator-response queue
    And  Validating schema of failed callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
