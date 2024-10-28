@orchestrator @unbindQueue @rmq
Feature: Unbind request queue from the exchange
  This feature unbinds the TINAA requests queue from the exchange before the tests are executed

  Scenario: Unbind request queue from the default exchange bng-svc-cont
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/bng_svc_controller_queue/bng_svc_controller_queue" for "DELETE"
    Then I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "bng_svc_controller_queue" queue "does not have" "consumer_rabbit_exchange" exchange as source

  Scenario: Unbind request queue from the default exchange cs-portal-queue
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/cs_portal_queue/cs_portal_queue" for "DELETE"
    Then I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "cs_portal_queue" queue "does not have" "consumer_rabbit_exchange" exchange as source

  Scenario: Unbind request queue from the default exchange evpn-svc-cont
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/evpn_svc_controller_queue/evpn_svc_controller_queue" for "DELETE"
    Then I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "evpn_svc_controller_queue" queue "does not have" "consumer_rabbit_exchange" exchange as source

  Scenario: Unbind request queue from the default exchange l2_topo
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/l2_topology_engine_queue/l2_topology_engine_queue" for "DELETE"
    Then I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "l2_topology_engine_queue" queue "does not have" "consumer_rabbit_exchange" exchange as source









