@tc52 @orchestrator
Feature: Create OLT onboarding config - Fail from L2
  This feature test the functionality related to create the OLT on-boarding config

   Scenario: TC 52 Create OLT onboarding config - Fail from L2
     Given I read test data for CS testcases
# 1/12 We send to Orch
     When "Publish" "tc_52_create_olt_onboarding_config_fail" message to "RMQ" "orchestrator" queue for Orchestrator
# 3/12 We send to Orch
     When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
     Then "Publish" "tc_52_create_olt_onboarding_config_l2_to_orchestrator_failed" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_52_create_olt_onboarding_config_orchestrator_to_portal_failed_l2" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
