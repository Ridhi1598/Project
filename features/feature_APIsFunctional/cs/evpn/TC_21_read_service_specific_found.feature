@tc5 @evpnController @cs
Feature:Read Evpn Services
   Evpn specific service needs to already exist

  Scenario: This scenario validates Read operation by sending a request to get a specific available service
    Given I read test data for CS testcases
    Then Sending a get-service request
    And Validating that callback is published in completed state in EVPN RMQ
    Then Validating get-service request callback
