@tc14 @orchestrator
Feature: Create OLT on-boarding config
  This feature test the functionality related to create the OLT on-boarding config

   Scenario: Create the OLT onboarding config
     Given I read test data for CS testcases
     When "Publish" "tc_14_create_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
     When I wait for "90" seconds for request to be timed out
     Then "Read" and validate that the "baseRequestId" "tc_49_create_olt_onboarding_config_orchestrator_to_portal_timeout_from_l2" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
