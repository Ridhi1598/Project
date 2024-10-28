@controller @unbindQueue @rmq @preSetup @demo
Feature: Unbind request queue from the exchange
  This feature unbinds the tinaa requests queue from the exchange before the tests are executed

  Scenario: Unbind request queue from the default exchange
    Given I set l3vpn "RMQ" url
    And I set api endpoint "api/bindings/%2F/e/l3vpn-ingestion/q/tinaa-l3vpn-request-callbacks/tinaa-l3vpn-request-callbacks" for "DELETE"
    When I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "api/exchanges/%2F/l3vpn-ingestion/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "tinaa-l3vpn-request-callbacks" queue "does not have" "l3vpn-ingestion" exchange as source