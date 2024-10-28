@tc74 @orchestrator
Feature: Delete OLT onboarding config - Fail from L2
  This feature validates that functionality related to unlock the BNG l2-resources

   Scenario: tc_74: Delete OLT onboarding config - Fail from L2
    Given I read test data for orchestrator testcases
    Then I validate that the request record should "exist" in the table "active_olts" by "clli_name" for orchestrator
    When "Publish" "tc_14_create_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "tc_74_delete_olt_onboarding_config_l2_to_orchestrator_first_request_failed" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_74_delete_olt_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator