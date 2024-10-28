Feature: Validate l3vpn controller timeout response for Update Node with audit true
  This features tests timeout of Update node scenario with audit true
  Scenario: Timeout in Update Node with audit true with MWR parameters
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
    Then Sending update-mwr-node with audit true payload to L3VPN via RMQ
    Then Validating that error callback is published to orchestrator-response queue
    And  Validating schema of error callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete

