Feature: Concurrency Control for Service
  This feature ensures that a VPN service creation process does not accept another request if
  it is already in progress. It aims to prevent concurrent creation of services to avoid conflicts,
  resource allocation issues, and potential data corruption.

  Scenario: Testcase for Concurrency Control during Service Creation

    Given I read test data for testcase
    Then Adding in-progress service to L3VPN es-record
    Then Validating that service-record is created in ES
    And Validating that service-record in-progress is set to True
    Then Sending a new service (CRUD) request but before that I will make sure it is not already in DB
    When Validating that service-record is not created in ES
    Then Sending create-service payload to L3VPN via RMQ
    Then Validating that request-record is in rejected state
    And Validating that error callback is published to orchestrator-response queue
    Then Validating schema of error callback published in orchestrator
    And Validating that error callback message in orchestrator-response queue contains Too many concurrent requests string
  Scenario: Delete the created service record from ES database
    Then Performing cleanup: service-delete
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
#    Then Validating that service-record is created in ES
