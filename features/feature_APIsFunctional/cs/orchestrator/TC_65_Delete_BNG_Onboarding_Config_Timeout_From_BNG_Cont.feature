@tc65 @orchestrator
Feature: Delete BNG onboarding config - Timeout from BNG cont
  This feature validates that functionality related to unlock the BNG l2-resources

  Scenario: Tc 65 Delete BNG onboarding config - Timeout from BNG cont
    Given I read test data for CS testcases
    When "Publish" "tc_18_delete_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    When I wait for "320" seconds for request to be timed out
    Then "Read" and validate that the "baseRequestId" "tc_65_delete_bng_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    Then I validate that the request record should "exist" in the table "active_bngs" by "bng_clli_group" for orchestrator
    And Validating that orch_external_request_tracker record is updated with timeout state
