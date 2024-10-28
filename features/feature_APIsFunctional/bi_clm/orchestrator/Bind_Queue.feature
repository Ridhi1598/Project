@orchestrator @bindQueue @rmq @postSetup
Feature: Bind request queue to the exchange
  This feature binds the tinaa requests queue back to the exchange after all the tests are executed

  Scenario: Bind request queue to the default exchange
    Given I set "RMQ" url
    And I set api endpoint "/api/bindings/%2F/e/com.telus.tinaa.bsaf.clm.bi/q/com.telus.tinaa.bsaf.clm.bi.ingestion.response" for "POST"
    And I Set POST request Body "bindQueue.json" for "com.telus.tinaa.bsaf.clm.bi.ingestion.response"
    When I send "POST" request
    And I validate expected response code "201" for "POST"
    And Validate response header "location" for "com.telus.tinaa.bsaf.clm.bi.ingestion.response/com.telus.tinaa.bsaf.clm.bi.ingestion.response"
    And I set api endpoint "/api/exchanges/%2F/com.telus.tinaa.bsaf.clm.bi/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue "has" "com.telus.tinaa.bsaf.clm.bi" exchange as source