@tc68 @orchestrator
Feature: Delete BNG onboarding config - Fail from EVPN cont
  This feature validates that functionality related to unlock the BNG l2-resources

   Scenario: Tc 68 Delete BNG onboarding config - Fail from EVPN cont
    Given I read test data for CS testcases
# 1/8 We send to Orch
    When "Publish" "tc_68_delete_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
# 2/8 Orch to BNG
    When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
# 3/8 We send to Orch
    Then "Publish" "tc_68_delete_bng_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
# 4/8 Orch to EVPN
    Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
# 5/8 We send to Orch
    When "Publish" "tc_68_delete_bng_onboarding_config_evpn_to_orchestrator_first_request_failed" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_68_delete_bng_onboarding_config_orchestrator_to_portal_failed_evpn" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    And Validating that orch_external_request_tracker record is updated with failed state
    And Validating that orch_bsaf_request_tracker record is updated with completed state