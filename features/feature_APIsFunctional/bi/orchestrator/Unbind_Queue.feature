@orchestrator @unbindQueue @rmq @preSetup @demo
Feature: Unbind request queue from the exchange
  This feature unbinds the tinaa requests queue from the exchange before the tests are executed

  Scenario: Unbind request queue from the default exchange
    Given I set BI "RMQ" url
    And I set api endpoint "/api/bindings/%2F/e/bi-ctrl/q/tinaa-bi-request-callbacks/tinaa-bi-request-callbacks" for "DELETE"
    When I send "DELETE" request
    And I validate expected response code "204" or "404" for "DELETE"
    Then I set api endpoint "/api/exchanges/%2F/bi-ctrl/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "tinaa-bi-request-callbacks" queue "does not have" "bi-ctrl" exchange as source