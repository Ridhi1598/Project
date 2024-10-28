@tc30 @orchestrator
Feature: Unlock BNG L2-resources - Failed
  This feature validates that functionality related to unlock the BNG l2-resources

   Scenario Outline: This scenario validate that the functionality related to unlock BNG l2-resources - Failed
    Given I read test data for CS testcases
    When "Publish" "<tc_num><portal_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "<tc_num><l2_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "<tc_num><orchestrator_to_portal>" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    And Validating that orch_bsaf_request_tracker record is updated with completed state
    And Validating that orch_external_request_tracker record is updated with completed state

    Examples:
     |tc_num | portal_to_orchestrator                                 | l2_to_orchestrator                                | orchestrator_to_portal                                |
     |tc_30   |_unlock_bng_l2_resources_portal_to_orchestrator_failed |_unlock_bng_l2_resources_l2_to_orchestrator_failed |_unlock_bng_l2_resources_orchestrator_to_portal_failed|


