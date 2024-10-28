@L2TopologyEngine @bindQueue @rmq
Feature: Bind request queue to the exchange
  This feature binds the tinaa requests queue back to the exchange after all the tests are executed

  Scenario: Bind request queue to the default exchange
    Given I set Consumer "RMQ" url
    And I set CS api endpoint "/api/bindings/%2F/e/rabbit_exchange/q/cs_portal_queue" for "POST"
    And I Set POST Consumer request Body "bindQueue.json" for "cs_portal_queue"
    When I send CS "POST" request
    And I validate consumer expected response code "201" for "POST"
    And Validate consumer response header "location" for "cs_portal_queue/cs_portal_queue"
    And I set CS api endpoint "/api/exchanges/%2F/rabbit_exchange/bindings/source" for "GET"
    When I send CS "GET" request
    And I validate consumer expected response code "200" for "GET"
    Then Validate that consumer "cs_portal_queue" queue "has" "rabbit_exchange" exchange as source