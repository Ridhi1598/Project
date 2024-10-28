Feature: Clear the queue of its contents
  This feature clears all the messages from the test queue before the tests are executed

  Scenario: Clear all the messages from the test queue
    Given I set "RMQ" url
    And I set api endpoint "/api/queues/%2F/bng_svc_controller_queue_test/contents" for "DELETE"
    When I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/queues/%2F/bng_svc_controller_queue_test/get" for "POST"
    And I Set POST request Body "rmq_get_message.json" for "bng_svc_controller_queue_test"
    And I send "POST" request
    And I validate expected response code "200" for "POST"
    And Validate that the queue is empty

  Scenario: Clear all the messages from the test queue
    Given I set "RMQ" url
    And I set api endpoint "/api/queues/%2F/cs_portal_queue_test/contents" for "DELETE"
    When I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/queues/%2F/cs_portal_queue_test/get" for "POST"
    And I Set POST request Body "rmq_get_message.json" for "cs_portal_queue_test"
    And I send "POST" request
    And I validate expected response code "200" for "POST"
    And Validate that the queue is empty

  Scenario: Clear all the messages from the test queue
    Given I set "RMQ" url
    And I set api endpoint "/api/queues/%2F/l2_topology_engine_queue_test/contents" for "DELETE"
    When I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/queues/%2F/l2_topology_engine_queue_test/get" for "POST"
    And I Set POST request Body "rmq_get_message.json" for "l2_topology_engine_queue_test"
    And I send "POST" request
    And I validate expected response code "200" for "POST"
    And Validate that the queue is empty

  Scenario: Clear all the messages from the test queue
    Given I set "RMQ" url
    And I set api endpoint "/api/queues/%2F/cs_orchestrator_queue_test/contents" for "DELETE"
    When I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/queues/%2F/cs_orchestrator_queue_test/get" for "POST"
    And I Set POST request Body "rmq_get_message.json" for "cs_orchestrator_queue_test"
    And I send "POST" request
    And I validate expected response code "200" for "POST"
    And Validate that the queue is empty