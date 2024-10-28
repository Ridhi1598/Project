@tc5 @evpnController @cs
Feature:Read Evpn Services
   Evpn services should not exist

  Scenario: This scenario validates Read operation by sending a request to get a non existing service
    Given I read test data for CS testcases
    Then Sending a get-non-existing-service request
    And Validating that callback is published in completed state in EVPN RMQ
    Then Validating get-non-existing-service request callback
