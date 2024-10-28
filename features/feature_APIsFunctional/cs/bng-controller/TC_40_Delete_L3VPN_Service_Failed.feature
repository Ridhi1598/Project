@tc40 @bngController
Feature: Delete the L3VPN Service - Failed
  This feature validates that functionality related to delete the L3VPN Service - Failed

   Scenario Outline: tc_40 : This scenario validate that the functionality related to delete the L3VPN Service - Failed
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "failed" state
    When Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "failed" state
    Then I validate that the request record should "exist" in the table "vpn_service" by "vpn_id"
    When I validate that the request record should "exist" in the table "vpn_node" by "vpn_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  | published                         |   bng_to_portal                             |
     |tc_40   | _delete_l3vpn_service_failed      |  _delete_l3vpn_service_bng_to_portal_failed |
