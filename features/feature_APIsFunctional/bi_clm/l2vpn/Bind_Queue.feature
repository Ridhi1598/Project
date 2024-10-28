@l3vpn @bindQueue @rmq @postSetup
Feature: Bind request queue to the exchange
  This feature binds the orchestrator response queue back to the exchange after all the tests are executed

  Scenario: Bind orchestrator response queue to the default exchange
    Given I set "RMQ" url
    And I set api endpoint "/api/bindings/%2F/e/com.telus.tinaa.bsaf.clm.bi/q/com.telus.tinaa.bsaf.clm.bi.orchestrator.response" for "POST"
    And I Set POST request Body "bindQueue.json" for "com.telus.tinaa.bsaf.clm.bi.orchestrator.response"
    When I send "POST" request
    And I validate expected response code "201" for "POST"
    And Validate response header "location" for "com.telus.tinaa.bsaf.clm.bi.orchestrator.response/com.telus.tinaa.bsaf.clm.bi.orchestrator.response"
    And I set api endpoint "/api/exchanges/%2F/com.telus.tinaa.bsaf.clm.bi/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "com.telus.tinaa.bsaf.clm.bi.orchestrator.response" queue "has" "com.telus.tinaa.bsaf.clm.bi" exchange as source

  Scenario: Bind orchestrator response queue to the default exchange
    Given I set "RMQ" url
    And I set api endpoint "/api/bindings/%2F/e/com.telus.tinaa.bsaf.clm.bi/q/com.telus.tinaa.bsaf.clm.bi.orchestrator.l2vpn.controller.request" for "POST"
    And I Set POST request Body "bindQueue.json" for "com.telus.tinaa.bsaf.clm.bi.orchestrator.l2vpn.controller.request"
    When I send "POST" request
    And I validate expected response code "201" for "POST"
    And Validate response header "location" for "com.telus.tinaa.bsaf.clm.bi.orchestrator.l2vpn.controller.request/com.telus.tinaa.bsaf.clm.bi.orchestrator.l2vpn.controller.request"
    And I set api endpoint "/api/exchanges/%2F/com.telus.tinaa.bsaf.clm.bi/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "com.telus.tinaa.bsaf.clm.bi.orchestrator.l2vpn.controller.request" queue "has" "com.telus.tinaa.bsaf.clm.bi" exchange as source