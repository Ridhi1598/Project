Feature: Validate l3vpn controller's delete operation
  This features validates a timed out delete request of vpn-service

  Scenario: Timeout occurs while deleting a VPN having only one node. Controller will trigger the ep without node_id param
    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to False
    Then Sending delete-service payload to L3VPN via RMQ
    Then Validating that error callback is published to orchestrator-response queue
    And  Validating schema of error callback published in orchestrator
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
