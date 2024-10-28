Feature: Validate l3vpn controller response for update Node with audit true
  This features tests update node with audit true
  Scenario: Update Node audit true
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
    Then Sending update-node with audit true payload to L3VPN via RMQ
#    Then validating that service record bandwidth is changed
    Then Validating that success callback is published to orchestrator-response queue
    And  Validating schema of success-audit callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete

    