@ingestionEngine @bindQueue @rmq
Feature: Bind request queue to the exchange
  This feature binds the tinaa requests queue back to the exchange after all the tests are executed

  Scenario: Bind request queue to the default exchange
    Given I set L3VPN "RMQ" url
    When I set api endpoint "api/bindings/%2F/e/l3vpn-ingestion/q/tinaa-l3vpn-requests" for "POST" for IE
    And I Set POST request Body "bindQueue.json" for "tinaa-l3vpn-requests" for IE
    When I send "POST" request for IE
    And Validate expected response code "201" for "POST" for IE
    And Validate response header "location" for "tinaa-l3vpn-requests/tinaa-l3vpn-requests" for IE
    And I set api endpoint "api/exchanges/%2F/l3vpn-ingestion/bindings/source" for "GET" for IE
    Then I send "GET" request for IE
    And Validate expected response code "200" for "GET" for IE
    And Validate that "tinaa-l3vpn-requests" queue "has" "l3vpn-ingestion" exchange as source for IE