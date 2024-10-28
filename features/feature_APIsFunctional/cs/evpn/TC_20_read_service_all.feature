@tc5 @evpnController @cs
Feature:Read Evpn Services
   Evpn services needs to already exist

  Scenario: This scenario validates Read operation by sending a request to get all available services
    Given I read test data for CS testcases
    Then Sending a get-all-service request
    And Validating that callback is published in completed state in EVPN RMQ
    Then Validating get-all-service request callback
