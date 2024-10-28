@tc1 @orchestrator
Feature: Get active BNGs
  This feature to get all the active BNGs

   Scenario Outline: Get all the active BNGs
    Given I read test data for CS testcases
    When "Publish" "<tc_num><portal_to_orchestrator>" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "<tc_num><orchestrator_to_portal>" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

    Examples:
    |tc_num | portal_to_orchestrator                | orchestrator_to_portal                     |
    |tc_1   |_get_active_bng_portal_to_orchestrator |_get_active_bng_orchestrator_to_portal      |
