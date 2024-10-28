@oltDecommission @rmq @preprod
Feature: Validate OLT decommission
  This features to validate the OLT Decommission process

  Scenario: Validate the OLT Decommission
    Given I set CS "RMQ" url
    And I set api endpoint "/api/exchanges/%2F/rabbit_exchange/publish" for "POST"
    And I Set Consumer POST request Body "olt_decommission_preprod.json" for decommission
    When I send "POST" request
    Then I extract the response code value
