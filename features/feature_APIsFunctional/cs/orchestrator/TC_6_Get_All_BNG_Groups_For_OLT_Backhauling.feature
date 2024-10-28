@tc6 @orchestrator
Feature: Get all BNG groups for OLT back-hauling
  This feature to get all BNG groups for OLT back-hauling

   Scenario Outline: Get all BNG groups for OLT back-hauling
    Given I read test data for CS testcases
    When "Publish" "<tc_num><portal_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "<tc_num><orchestrator_to_portal>" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

    Examples:
    |tc_num| portal_to_orchestrator                                         | orchestrator_to_portal                                           |
    |tc_6  |_get_all_bng_groups_for_olt_backhauling_portal_to_orchestrator |_get_all_bng_groups_for_olt_backhauling_orchestrator_to_portal|
