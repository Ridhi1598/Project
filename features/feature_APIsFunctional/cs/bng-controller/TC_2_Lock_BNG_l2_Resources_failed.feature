@tc2 @bngController
Feature: Lock BNG L2-resources
  This feature validates that functionality related to Lock the BNG l2-resources - Failed

   Scenario Outline: tc_2: This scenario validate that the functionality related to lock BNG l2-resources
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    Then "Publish" "<tc_num><l2_to_bng>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "cs_portal_test" queue for BNG

    Examples:
     |tc_num | published                      | l2_to_bng                             | bng_to_portal                              |
     |tc_2   | _lock_bng_l2_resources_failed | _lock_bng_resources_l2_to_bng_failed | _lock_bng_l2_resources_bng_to_portal_failed |


