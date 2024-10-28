Feature: Concurrency Control for Service
  This feature ensures that a VPN service update process does not accept another request if
  there is already an update vpn service request in progress. It aims to prevent concurrent updation of services to avoid conflicts,
  resource allocation issues, and potential data corruption.

  Scenario: Testcase for Concurrency Control during VPN Service Update

    Given I read test data for testcase
    Then Adding in-progress service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to True
    Then Sending update-node payload via RMQ
    Then Validating that request-record is in rejected state
    And Validating that error callback is published to orchestrator-response queue
    Then Validating schema of error callback published in orchestrator
    And Validating that error callback message in orchestrator-response queue contains too many concurrent requests string
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
