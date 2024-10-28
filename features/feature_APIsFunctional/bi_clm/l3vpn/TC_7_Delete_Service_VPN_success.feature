Feature: Validate l3vpn controller's delete operation
  This features validates successful deletion of vpn-service

  Scenario: Delete a VPN having only one node. Controller should trigger the ep without node_id param
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
    Then Sending delete-service payload to L3VPN via RMQ
    Then Validating that in-process callback is published to orchestrator-response queue
    Then Validating that success callback is published to orchestrator-response queue
    And  Validating schema of success callback published in orchestrator
    Then Validating that service-record is not created in ES
