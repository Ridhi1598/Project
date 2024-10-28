@tc43 @orchestrator
Feature: Validate OLT-BNG L2 resources failed from EVPN
  This feature test the functionality related to Validate the OLT-BNG L2 resources

   Scenario: Validate OLT-BNG L2 resources failed from EVPN

    Given I read test data for CS testcases
    When "Publish" "tc_47_create_bng_onboarding_config_failed_from_bng" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    Then "Publish" "tc_47_create_bng_onboarding_config_bng_to_orchestrator_failed_from_bng" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_47_create_bng_onboarding_config_orchestrator_to_portal_failed_from_bng" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

