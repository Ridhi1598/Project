@tc5 @orchestrator
Feature: Get all OLTs in L2 engine with their WF status- Success
  This feature to get all OLTs in L2 engine with their WF status

   Scenario Outline: Get all OLTs in L2 engine with their WF status - Success
    Given I read test data for CS testcases
    When "Publish" "<tc_num><portal_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "<tc_num><l2_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "<tc_num><orchestrator_to_portal>" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

    Examples:
    |tc_num |portal_to_orchestrator                                           |l2_to_orchestrator                                          | orchestrator_to_portal                                          |
    |tc_5   |_get_all_olt_in_l2_with_wf_status_portal_to_orchestrator_success |_get_all_olt_in_l2_with_wf_status_l2_to_orchestrator_success|_get_all_olt_in_l2_with_wf_status_orchestrator_to_portal_success |
