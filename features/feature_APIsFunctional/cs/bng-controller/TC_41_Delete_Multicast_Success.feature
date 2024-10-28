@tc41 @bngController
Feature: Delete Multicast Service
  This feature validates that functionality related to delete the BNG dry run

   Scenario Outline: tc_41 : This scenario validate that the functionality related to delete Multicast Service
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "not-exist" in the table "vpn_service" by "vpn_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num | published                    |  bng_to_portal                           |
     |tc_41   | _delete_multicast_success   |  _delete_multicast_bng_to_portal_success |