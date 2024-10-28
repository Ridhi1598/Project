@controller @bindQueue @rmq @postSetup @demo
Feature: Bind request queue to the exchange
  This feature binds the tinaa requests queue back to the exchange after all the tests are executed

  Scenario: Bind request queue to the default exchange
    Given I set l3vpn "RMQ" url
    And I set api endpoint "api/bindings/%2F/e/l3vpn-ingestion/q/tinaa-l3vpn-request-callbacks" for "POST"
    And I Set POST request Body "bindQueue.json" for "tinaa-l3vpn-request-callbacks"
    When I send "POST" request
    And I validate expected response code "201" for "POST"
    And Validate response header "location" for "tinaa-l3vpn-request-callbacks/tinaa-l3vpn-request-callbacks"
    And I set api endpoint "api/exchanges/%2F/l3vpn-ingestion/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "tinaa-l3vpn-request-callbacks" queue "has" "l3vpn-ingestion" exchange as source