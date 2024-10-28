@tc2 @orchestrator
Feature: Get all the active OLTs mapped with the BNGs
  This feature to get all the active OLTs which are mapped with the BNG pairs

   Scenario Outline: Get all the Active OLTs mapped with BNG
    Given I read test data for CS testcases
    When "Publish" "<tc_num><portal_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "<tc_num><orchestrator_to_portal>" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

    Examples:
    |tc_num| portal_to_orchestrator                       | orchestrator_to_portal                     |
    |tc_2  |_getActiveOlt_success_portal_to_orchestrator | _getActiveOlt_success_orchestrator_to_portal|
