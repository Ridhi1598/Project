Feature: Validate l3vpn controller response for delete Node audit true timeout
  This features tests delete node scenario with audit timeout
  Scenario: Delete Node with audit timeout
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
    When Validating that service-record is not created in ES
    Then Sending create-node payload to L3VPN via RMQ
    And Validating that request-record is in completed state
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
    Then Validating that service-record is created in ES
    Then Validating that service-record in-progress is set to False
    Then Sending delete-node with audit true payload to L3VPN via RMQ
    Then Validating that error callback is published to orchestrator-response queue
    And  Validating schema of failed callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete