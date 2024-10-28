Feature: Validate l3vpn controller failed response for Update Node audit true
  This features tests failure of Update node scenario with mwr parameters
  Scenario: Failure in Update with audit true Node with MWR parameters
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
    Then Sending update-mwr-node with audit true payload to L3VPN via RMQ
    Then validating that service record bandwidth is not changed
    Then Validating that error callback is published to orchestrator-response queue
    And  Validating schema of error callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
