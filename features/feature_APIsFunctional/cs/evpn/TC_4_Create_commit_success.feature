@tc4 @evpnController @cs
Feature: Commit previous created evpn request using request-id
  Commit previous created evpn dry run request

  Scenario: This scenario validates commit request getting successfully executed
    Given I read test data for CS testcases
    Then Sending a create-dry-run request
    And Validating that callback is published in completed state in EVPN RMQ
    Then Sending a create-commit request
    Then Fetching external_id from evpn_external_request_tracker
    Then Reading callback published from l2 in l2 topology RMQ
    And Publishing callback fetched from l2 topology queue to EVPN RMQ
    Then Validating that evpn_external_request_tracker record is updated with completed state
    Then Validating that evpn_bsaf_request_tracker record is updated with completed state
    And Validating that callback is published in completed state in EVPN RMQ
    And Validating that evpn_service record is created
    And Validating schema of success callback published in EVPN

  Scenario: Clean-up
    When Sending a delete-service request
    Then Validating that evpn_service record is-not created
    And Validating that callback is published in completed state in EVPN RMQ

# a payload will be sent to l2 topology from evpn then we have to get that payload from l2 topology test queue
# using request id, we will fetch and store the "path" key, for success scenarios a msg should be published into evpn
# consume queue so we have to read that msg using request id and path which we stored earlier