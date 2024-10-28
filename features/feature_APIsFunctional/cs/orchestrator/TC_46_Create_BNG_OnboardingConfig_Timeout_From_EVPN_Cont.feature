@tc46 @orchestrator
Feature: Create BNG onboarding config - Timeout from EVPN cont
  This feature test the functionality related to create the BNG onboarding config

   Scenario: TC 46 Create BNG onboarding config - Timeout from EVPN cont
     Given I read test data for CS testcases
     When "Publish" "tc_46_create_bng_onboarding_config_timeout" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     When "Publish" "tc_46_create_bng_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_46_create_bng_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
