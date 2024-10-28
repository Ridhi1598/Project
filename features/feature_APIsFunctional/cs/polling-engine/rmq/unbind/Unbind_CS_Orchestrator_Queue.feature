@bngController @unbindQueue @rmq
Feature: Unbind request queue from the exchange
  This feature unbinds the TINAA requests queue from the exchange before the tests are executed

  Scenario: Unbind request queue from the default exchange
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/cs_orchestrator_queue/cs_orchestrator_queue" for "DELETE"
    Then I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "cs_orchestrator_queue" queue "does not have" "consumer_rabbit_exchange" exchange as source


