@tc51 @orchestrator
Feature: Create OLT onboarding config - timeout from EVPN cont
  This feature test the functionality related to create the OLT on-boarding config

   Scenario: tc_51 :Create OLT onboarding config - timeout from EVPN cont
     Given I read test data for orchestrator testcases
     When "Publish" "tc_14_create_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
     Then "Publish" "tc_14_create_olt_onboarding_config_l2_to_orchestrator_success" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     When I wait for "350" seconds for request to be timed out
     Then "Read" and validate that the "baseRequestId" "tc_51_create_olt_onboarding_config_orchestrator_to_portal_timeout_from_evpn" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
