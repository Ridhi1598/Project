@l3VPN @unbindQueue @rmq @preSetup
Feature: Unbind request queue from the exchange
  This feature unbinds the orchestrator response queue from the exchange before the tests are executed

  Scenario: Unbind orchestrator response queue from the default exchange
    Given I set "RMQ" url
    And I set api endpoint "/api/bindings/%2F/e/com.telus.tinaa.bsaf.clm.bi/q/com.telus.tinaa.bsaf.clm.bi.orchestrator.response/com.telus.tinaa.bsaf.clm.bi.orchestrator.response" for "DELETE"
    When I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "/api/exchanges/%2F/com.telus.tinaa.bsaf.clm.bi/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "com.telus.tinaa.bsaf.clm.bi.orchestrator.response" queue "does not have" "com.telus.tinaa.bsaf.clm.bi" exchange as source