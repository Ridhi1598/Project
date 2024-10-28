@tc1 @bngController
Feature: Lock BNG L2-resources
  This feature validates that functionality related to Lock the BNG l2-resources

   Scenario Outline: tc_1: This scenario validate that the functionality related to lock BNG l2-resources
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    Then "Publish" "<tc_num><l2_to_bng>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "cs_portal_test" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state

    Examples:
     |tc_num | published                      | l2_to_bng                                | bng_to_portal                                     |
     |tc_1   | _lock_bng_l2_resources_success | _lock_bng_l2_resources_l2_to_bng_success | _lock_bng_l2_resources_bng_to_portal_success |


