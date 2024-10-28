@evpn @bindQueue @rmq @postSetup
Feature: Bind request queue to the exchange
  This feature binds the orchestrator response queue back to the exchange after all the tests are executed

  Scenario: Bind request queue to the default exchange
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/cs_orchestrator_queue" for "POST"
    Then I Set POST request Body "bindQueue.json" for "cs_orchestrator_queue"
    When I send "POST" request
    Then I validate expected response code "201" for "POST"
    And Validate response header "location" for "cs_orchestrator_queue/cs_orchestrator_queue"
    When I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    When I validate expected response code "200" for "GET"
    Then Validate that "cs_orchestrator_queue" queue "has" "consumer_rabbit_exchange" exchange as source

  Scenario: Bind request queue to the default exchange
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/l2_topology_engine_queue" for "POST"
    Then I Set POST request Body "bindQueue.json" for "l2_topology_engine_queue"
    When I send "POST" request
    Then I validate expected response code "201" for "POST"
    And Validate response header "location" for "l2_topology_engine_queue/l2_topology_engine_queue"
    When I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    When I validate expected response code "200" for "GET"
    Then Validate that "l2_topology_engine_queue" queue "has" "consumer_rabbit_exchange" exchange as source

  Scenario: Bind request queue to the default exchange
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/evpn_svc_controller_queue" for "POST"
    Then I Set POST request Body "bindQueue.json" for "evpn_svc_controller_queue"
    When I send "POST" request
    Then I validate expected response code "201" for "POST"
    And Validate response header "location" for "evpn_svc_controller_queue/evpn_svc_controller_queue"
    When I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    When I validate expected response code "200" for "GET"
    Then Validate that "evpn_svc_controller_queue" queue "has" "consumer_rabbit_exchange" exchange as source