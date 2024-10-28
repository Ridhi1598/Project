@tc55 @orchestrator
Feature: Push BNG onboarding config - Timeout from BNG cont
  This feature validates that functionality related to unlock the BNG l2-resources

  Scenario: TC 55 Push BNG onboarding config - Timeout from BNG cont
    Given I read test data for CS testcases

    When "Publish" "tc_55_push_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_55_push_bng_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
