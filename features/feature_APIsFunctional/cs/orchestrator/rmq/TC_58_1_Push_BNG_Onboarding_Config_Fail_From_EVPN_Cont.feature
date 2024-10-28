@tc30 @orchestrator
Feature: Push BNG onboarding config - Fail from EVPN cont
  This feature validates that functionality related to unlock the BNG l2-resources

  Scenario: tc_13 : Create the BNG onboarding config
   Given I read test data for orchestrator testcases
   When "Publish" "tc_13_create_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
   Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
   When "Publish" "tc_13_create_bng_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
   Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
   When "Publish" "tc_13_create_bng_onboarding_config_evpn_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
   Then "Read" and validate that the "second" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
   When "Publish" "tc_13_create_bng_onboarding_config_bng_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
   Then "Read" and validate that the "baseRequestId" "tc_13_create_bng_onboarding_config_orchestrator_to_portal_success" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

   Scenario: tc_15:  TC 58 Push BNG Onboarding Config Fail From EVPN Cont
     Given I read test data for orchestrator testcases
     When "Publish" "tc_15_push_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     Then "Publish" "tc_15_push_bng_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     When "Publish" "tc_58_push_bng_onboarding_config_evpn_to_orchestrator_first_request_failed" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_58_push_bng_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
     Then I dump the cs_orchestrator object