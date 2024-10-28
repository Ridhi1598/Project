@orchestrator @createQueue @rmq @preSetup
Feature: Clear the queue of its contents
  This feature clears all the messages from the test queue before the tests are executed

  Scenario: Check if callback queue exists
    Given I set "RMQ" url for "cs"
    And I set api endpoint "/api/queues/%2F/evpn_svc_controller_queue-test" for "GET"
    When I send "GET" request
    Then I extract the response code value
    And I validate "evpn_svc_controller_queue-test" queue is binded to "consumer_rabbit_exchange" exchange
    Given I validate bind status from the previous step
    And I set api endpoint "/api/queues/%2F/evpn_svc_controller_queue-test" for "PUT"
    And I Set PUT request Body "rmq_create_queue.json" for "evpn_svc_controller_queue-test"
    Then I send "PUT" request
    When I validate expected response code "201" or "204" for "PUT"
    Given I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/evpn_svc_controller_queue-test" for "POST"
    And I Set POST request Body "bindQueue.json" for "evpn_svc_controller_queue-test"
    When I send "POST" request
    And I validate expected response code "201" for "POST"
    And Validate response header "location" for "evpn_svc_controller_queue-test/evpn_svc_controller_queue-test"
    And I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "evpn_svc_controller_queue-test" queue "has" "consumer_rabbit_exchange" exchange as source