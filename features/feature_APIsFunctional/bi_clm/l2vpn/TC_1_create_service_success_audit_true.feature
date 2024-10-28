Feature: Validate mediation response for validate resource request
  Executor returns resource request response successfully but validation fails

  Scenario: Resource validation request with PW,LAg and VPLS success response from Executor but validation fails
    Given I read test data for testcase
    Then Sending create-l2vpn-service to l2vpn controller
#    Then Validating that evpn_bsaf_request_tracker record is created with failed state
#    Then Validating that evpn_external_request_tracker record is created with completed state
#    And Validating that callback is published in failed state in EVPN RMQ
#    And Validating schema of rv-pw-lag-vpls-failed callback published in EVPN
#    Then Validating that request-record is in submitted state
#    And Validating that in-process callback is published to orchestrator-response queue
#    Then Validating schema of in-process callback published in orchestrator
#    Then Validating that service-record is created in ES
##    And Validating that service-record in-progress is set to True
#    Then Validating that callback is received for VALIDATE_RESOURCES in completed state
#    And Validating that callback is received for CREATE_PROFILES in completed state
#    And Validating that callback is received for NODE in completed state
#    Then Validating that request-record state is completed
#    Then Validating that service-record in-progress is set to False
#    Then Validating that success callback is published to orchestrator-response queue
#    And  Validating schema of success callback published in orchestrator
#  Scenario: Delete the created service record from ES database
#    Then Performing cleanup: service-delete