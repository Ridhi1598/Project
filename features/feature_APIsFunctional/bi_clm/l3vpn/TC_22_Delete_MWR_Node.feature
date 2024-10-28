Feature: Validate l3vpn controller response for delete Node with mwr params
  This features tests delete node scenario with mwr parameters
  Scenario: Delete Node with MWR parameters
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
    Then Sending create-node payload with mwr param to L3VPN via RMQ
    Then Validating that request-record is in completed state
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
    Then Validating that service-record is created in ES
    Then Validating that service-record in-progress is set to False
    Then Sending delete-mwr-node payload to L3VPN via RMQ
    Then Validating that success callback is published to orchestrator-response queue
    And  Validating schema of success callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
