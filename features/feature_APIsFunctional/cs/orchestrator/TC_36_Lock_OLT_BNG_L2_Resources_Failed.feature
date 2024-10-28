@tc36 @orchestrator
Feature: Lock OLT-BNG L2 resources - Failed
  This feature test the functionality related to Lock the OLT-BNG L2 resources - Failed

   Scenario: Lock OLT-BNG L2 resources - Failed
    Given I read test data for CS testcases
    When "Publish" "tc_36_lock_the_olt_bng_l2_resources_failed" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    When "Publish" "tc_36_lock_the_olt_bng_l2_resources_l2_to_orchestrator_first_request_failed" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_36_lock_the_olt_bng_l2_resources_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator



