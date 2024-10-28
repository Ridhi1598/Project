@L2TopologyEngine @unbindQueue @rmq
Feature: Unbind request queue from the exchange
  This feature unbinds the TINAA requests queue from the exchange before the tests are executed

 Scenario: Unbind request queue from the default exchange
    Given I set Consumer "RMQ" url
    And I set CS api endpoint "/api/bindings/%2F/e/rabbit_exchange/q/cs_portal_queue/cs_portal_queue" for "DELETE"
    When I send CS "DELETE" request
    And I validate consumer expected response code "204" for "DELETE"
    And I set CS api endpoint "/api/exchanges/%2F/rabbit_exchange/bindings/source" for "GET"
    When I send CS "GET" request
    And I validate consumer expected response code "200" for "GET"
    And Validate that consumer "cs_portal_queue" queue "does not have" "rabbit_exchange" exchange as source