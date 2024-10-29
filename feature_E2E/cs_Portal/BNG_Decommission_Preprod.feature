@bngDecommission @rmq @preprod
Feature: Validate BNG decommission
  This features to validate the BNG Decommission process

  Scenario: Validate the BNG Decommission
    Given I set CS "RMQ" url
    And I set api endpoint "/api/exchanges/%2F/rabbit_exchange/publish" for "POST"
    And I Set Consumer POST request Body "bng_decommission_preprod.json" for decommission
    When I send "POST" request
    Then I extract the response code value
