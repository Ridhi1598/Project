@tc12 @orchestrator
Feature: Validate OLT-BNG L2 resources
  This feature test the functionality related to Validate the OLT-BNG L2 resources

   Scenario: Validate OLT-BNG L2 resources
    Given I read test data for CS testcases
    When "Publish" "tc_12_validate_olt_bng_l2_resources_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "tc_12_validate_olt_bng_l2_resources_l2_to_orchestrator_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
    Then "Publish" "tc_12_validate_olt_bng_l2_resources_orchestrator_to_evpn_success" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_12_validate_olt_bng_l2_resources_orchestrator_to_portal_success" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    And Validating that orch_external_request_tracker record is updated with completed state
    And Validating that orch_bsaf_request_tracker record is updated with completed state


