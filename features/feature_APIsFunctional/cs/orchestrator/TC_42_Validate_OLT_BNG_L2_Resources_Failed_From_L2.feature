@tc42 @orchestrator
Feature: Validate OLT-BNG L2 resources from L2
  This feature test the functionality related to Validate the OLT-BNG L2 resources

   Scenario: Validate OLT-BNG L2 resources from L2

    Given I read test data for CS testcases
    When "Publish" "tc_42_validate_olt_bng_l2_resources_failed_from_L2" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    When "Publish" "tc_42_validate_olt_bng_l2_resources_l2_to_orchestrator_failed_from_L2" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_42_validate_olt_bng_l2_resources_orchestrator_to_portal_failed_from_L2" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

