@tc54 @orchestrator
Feature: Create OLT onboarding config - Fail from EVPN cont
  This feature test the functionality related to create the OLT on-boarding config

   Scenario: tc_54 :Create OLT onboarding config - Fail from EVPN cont
     Given I read test data for orchestrator testcases
     When "Publish" "tc_14_create_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
     Then "Publish" "tc_14_create_olt_onboarding_config_l2_to_orchestrator_success" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     Then "Publish" "tc_54_create_olt_onboarding_config_evpn_to_orchestrator_first_request_failed" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_54_create_olt_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
