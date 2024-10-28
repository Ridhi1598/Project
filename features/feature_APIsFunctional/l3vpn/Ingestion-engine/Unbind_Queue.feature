@controller @unbindQueue @rmq @preSetup
Feature: Unbind request queue from the exchange
  This feature unbinds the tinaa requests queue from the exchange before the tests are executed

  Scenario: Unbind request queue from the default exchange
    Given I set L3VPN "RMQ" url
    When I set api endpoint "api/bindings/%2F/e/l3vpn-ingestion/q/tinaa-l3vpn-requests/tinaa-l3vpn-requests" for "DELETE" for IE
    Then I send "DELETE" request for IE
    And  Validate expected response code "204" for "DELETE" for IE
    Then I set api endpoint "api/exchanges/%2F/l3vpn-ingestion/bindings/source" for "GET" for IE
    Then I send "GET" request for IE
    And Validate expected response code "200" for "GET" for IE
    And Validate that "tinaa-l3vpn-requests" queue "does not have" "l3vpn-ingestion" exchange as source for IE