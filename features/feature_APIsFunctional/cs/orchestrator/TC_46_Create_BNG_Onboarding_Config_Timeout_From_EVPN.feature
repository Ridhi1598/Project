@tc46 @orchestrator
Feature: Validate OLT-BNG L2 resources timeout from EVPN
  This feature test the functionality related to Validate the OLT-BNG L2 resources timeout from EVPN

   Scenario: Validate OLT-BNG L2 resources timeout from EVPN
     Given I read test data for CS testcases
     When "Publish" "tc_46_create_bng_onboarding_config_timeout_from_evpn" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     When "Publish" "tc_46_create_bng_onboarding_config_bng_to_orchestrator_timeout_from_evpn" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     Then I wait for "350" seconds for request to be timed out
     Then "Read" and validate that the "baseRequestId" "tc_46_create_bng_onboarding_config_orchestrator_to_portal_timeout_from_evpn" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

