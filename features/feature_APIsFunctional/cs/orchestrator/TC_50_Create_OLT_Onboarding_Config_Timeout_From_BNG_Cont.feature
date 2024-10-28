@tc50 @orchestrator
Feature: Create OLT onboarding config - timeout from BNG cont
  This feature test the functionality related to create the OLT on-boarding config

  Scenario: TC 50 Create OLT onboarding config - timeout from BNG cont
    Given I read test data for CS testcases
    When "Publish" "tc_14_create_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "tc_14_create_olt_onboarding_config_l2_to_orchestrator_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
    Then "Publish" "tc_14_create_olt_onboarding_config_evpn_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    Then I wait for "320" seconds for request to be timed out
    Then "Read" and validate that the "baseRequestId" "tc_50_create_olt_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
