Feature: Concurrency Control for Service
  This feature ensures that a Node deletion process does not accept another request if
  it is already in progress. It aims to prevent concurrent deletion of nodes to avoid conflicts,
  resource allocation issues, and potential data corruption.

  Scenario: Testcase for Concurrency Control during Node Deletion

    Given I read test data for testcase
    Then Adding service to L3VPN es-record
    Then Validating that service-record is created in ES
    Then Sending create-node payload to L3VPN via RMQ
    Then Validating that service-record is created in ES
    Then Validating that service-record in-progress is set to False
    And Adding in-progress service to L3VPN es-record
    Then Validating that service-record in-progress is set to True
    And Sending delete-node payload to L3VPN via RMQ
    Then Validating that request-record is in rejected state
    And Validating that error callback is published to orchestrator-response queue
    Then Validating schema of error callback published in orchestrator
    And Validating that error callback message in orchestrator-response queue contains too many concurrent requests string
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete