@tc24 @orchestrator
Feature: Get OLTs that are available for on-boarding - Failed
  This feature to get OLTs that are available for on-boarding

   Scenario Outline: Get OLTs that are available for on-boarding - Failed
    Given I read test data for CS testcases
    When "Publish" "<tc_num><portal_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "<tc_num><l2_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "<tc_num><orchestrator_to_portal>" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

    Examples:
    |tc_num |portal_to_orchestrator                   |l2_to_orchestrator                                          | orchestrator_to_portal                                         |
    |tc_24  |_get_olt_available_for_onboarding_failed |_get_olt_available_for_onboarding_l2_to_orchestrator_failed |_get_olt_available_for_onboarding_orchestrator_to_portal_failed |
