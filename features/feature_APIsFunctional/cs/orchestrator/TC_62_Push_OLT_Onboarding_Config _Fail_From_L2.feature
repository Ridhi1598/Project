@tc62 @orchestrator
Feature: Push OLT onboarding config - Fail from L2 cont
  This feature validates that functionality related to unlock the BNG l2-resources

   Scenario: TC 62 Push OLT onboarding config - Fail from L2 cont
    Given I read test data for CS testcases
#1/12 We send to Orch
     When "Publish" "tc_62_push_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
#2/12 Orch to EVPN
#3/12 We send to Orch
     Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     When "Publish" "tc_62_push_olt_onboarding_config_evpn_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
# 4/12 Orch to BNG
# 5/12 We send to Orch
     When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     Then "Publish" "tc_62_push_olt_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
# 6/12 Orch sends to EVPN 
# 7/12 We send to Orch
     When "Read" and validate that the "second" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     Then "Publish" "tc_62_push_olt_onboarding_config_evpn_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
# 8/12 Orch to BNG
# 9/12 We send to Orch
     When "Read" and validate that the "second" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     Then "Publish" "tc_62_push_olt_onboarding_config_bng_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
# 10/12 Orch to L2 
# 11/12 We send to Orch
     When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
     Then "Publish" "tc_62_push_olt_onboarding_config_l2_to_orchestrator_failed" message to "RMQ" "orchestrator" queue for Orchestrator
# 12/12 Orch to Portal
     Then "Read" and validate that the "baseRequestId" "tc_62_push_olt_onboarding_config_orchestrator_to_portal_failed_l2" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
     And Validating that orch_external_request_tracker record is updated with completed state
     And Validating that orch_external_request_tracker record is updated with failed state
     And Validating that orch_bsaf_request_tracker record is updated with completed state
