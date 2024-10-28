@tc53 @orchestrator
Feature: Create OLT onboarding config - Fail from BNG
  This feature test the functionality related to create the OLT onboarding config - Fail from BNG

   Scenario: Create OLT onboarding config - Fail from BNG
     Given I read test data for CS testcases
     When "Publish" "tc_53_create_olt_onboarding_config_failed_from_bng" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
     Then "Publish" "tc_53_create_olt_onboarding_config_l2_to_orchestrator" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     Then "Publish" "tc_53_create_olt_onboarding_config_evpn_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     Then "Publish" "tc_53_create_olt_onboarding_config_bng_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator     
     Then "Read" and validate that the "baseRequestId" "tc_53_create_olt_onboarding_config_orchestrator_to_portal_failed_from_bng" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
