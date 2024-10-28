@controller @bindQueue @rmq @postSetup
Feature: Bind request queue to the exchange
  This feature binds the tinaa requests queue back to the exchange after all the tests are executed

  Scenario: Bind request queue to the default exchange
    Given I set BI "RMQ" url
    And I set api endpoint "/api/bindings/%2F/e/bi-ctrl/q/tinaa-bi-requests" for "POST"
    And I Set POST request Body "bindQueue.json" for "tinaa-bi-requests"
    When I send "POST" request
    And I validate expected response code "201" for "POST"
    And Validate response header "location" for "tinaa-bi-requests/tinaa-bi-requests"
    And I set api endpoint "/api/exchanges/%2F/bi-ctrl/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "tinaa-bi-requests" queue "has" "bi-ctrl" exchange as source