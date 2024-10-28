@tc70 @orchestrator
Feature: Delete OLT onboarding config - Timeout from BNG
  This feature validates that functionality related to unlock the BNG l2-resources

  Scenario: TC 70 Delete OLT onboarding config - Timeout from BNG
    Given I read test data for CS testcases
    When "Publish" "tc_19_delete_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "tc_19_delete_olt_onboarding_config_l2_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    When I wait for "320" seconds for request to be timed out
    Then "Read" and validate that the "baseRequestId" "tc_70_delete_olt_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    Then I validate that the request record should "exist" in the table "active_olts" by "clli_name" for orchestrator
    And Validating that orch_external_request_tracker record is updated with timeout state
