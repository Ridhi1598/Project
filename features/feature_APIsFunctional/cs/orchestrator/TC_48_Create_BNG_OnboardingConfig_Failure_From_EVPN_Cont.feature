@tc48 @orchestrator
Feature: Create BNG onboarding config - Failure from EVPN cont
  This feature test the functionality related to create the BNG onboarding config

   Scenario: tc_48 :Create BNG onboarding config - Failure from EVPN cont
     Given I read test data for orchestrator testcases
     When "Publish" "tc_13_create_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     When "Publish" "tc_13_create_bng_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     When "Publish" "tc_48_create_bng_onboarding_config_evpn_to_orchestrator_first_request_failed" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_48_create_bng_onboarding_config_orchestrator_to_portal_failed_from_evpn" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
