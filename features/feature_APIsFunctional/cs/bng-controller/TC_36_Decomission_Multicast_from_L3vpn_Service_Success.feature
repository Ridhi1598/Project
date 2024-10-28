@tc36 @bngController
Feature: Decommission Multicast_Node request
  This feature validates Decommission Multicast_Node request 

   Scenario Outline: tc_36 : Decommission Multicast_Node from L3vpn
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num | published                          |  bng_to_orchestrator                           |
     |tc_36   | _decommission_L3_nodes_success   |  _decommission_Multicast_Node_bng_to_orchestrator_success |


