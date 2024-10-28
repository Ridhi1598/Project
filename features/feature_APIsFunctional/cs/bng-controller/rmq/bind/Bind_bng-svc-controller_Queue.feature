@bngController @bindQueue @rmq
Feature: Bind request queue to the exchange
  This feature binds the bng publish queue to its exchange as a pre requisite

  Scenario: Bind request queue to the default exchange
    Given I set "RMQ" url
    When I set api endpoint "/api/bindings/%2F/e/consumer_rabbit_exchange/q/bng_svc_controller_queue" for "POST"
    Then I Set POST request Body "bindQueue.json" for "bng_svc_controller_queue"
    When I send "POST" request
    Then I validate expected response code "201" for "POST"
    And Validate response header "location" for "bng_svc_controller_queue/bng_svc_controller_queue"
    When I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/bindings/source" for "GET"
    Then I send "GET" request
    When I validate expected response code "200" for "GET"
    Then Validate that "bng_svc_controller_queue" queue "has" "consumer_rabbit_exchange" exchange as source