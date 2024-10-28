Feature: Validate l3vpn controller response for create service request
  This features validates l3vpn controller response for BI Day 1 Profiles exist + SE Devices doesn't exist

  Scenario: Create Service request with failure response from l3vpn controller for BI Day 1 Profiles exist + SE Devices don't exist
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
    Then Validating that service-record is not created in ES
    Then Sending create-service payload to L3VPN via RMQ
    Then Validating that callback is received for VALIDATE_RESOURCES in completed state
    And Validating that callback is received for CREATE_PROFILES in completed state
    And Validating that callback is received for NODE in completed state
    Then Validating that request-record state is completed
    Then Validating that service-record in-progress is set to False
    Then Validating that success callback is published to orchestrator-response queue
    And  Validating schema of success callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
