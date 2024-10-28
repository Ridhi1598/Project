@tc71 @orchestrator
Feature: Delete OLT onboarding config - Timeout from L2
  This feature validates that functionality related to unlock the BNG l2-resources

  Scenario: tc_71: Delete OLT onboarding config - Timeout from L2
    Given I read test data for orchestrator testcases
    Then I validate that the request record should "exist" in the table "active_olts" by "clli_name" for orchestrator
    When "Publish" "tc_14_create_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    When I wait for "90" seconds for request to be timed out
    Then "Read" and validate that the "baseRequestId" "tc_71_delete_olt_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
