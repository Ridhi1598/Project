@tc11 @orchestrator
Feature: Unlock OLT-BNG L2 resources
  This feature test the functionality related to Unlock the OLT-BNG L2 resources

   Scenario: Unlock OLT-BNG L2 resources
    Given I read test data for CS testcases
    When "Publish" "tc_11_unlock_the_olt_bng_l2_resources_success" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "tc_11_unlock_the_olt_bng_l2_resources_l2_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "second" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "tc_11_unlock_the_olt_bng_l2_resources_l2_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_11_unlock_the_olt_bng_l2_resources_orchestrator_to_portal_success" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    And Validating that orch_external_request_tracker record is updated with completed state
    And Validating that orch_bsaf_request_tracker record is updated with completed state


