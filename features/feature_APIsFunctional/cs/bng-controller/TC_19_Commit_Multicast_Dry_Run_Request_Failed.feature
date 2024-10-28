@tc19 @bngController
Feature: Commit create Multicast dry run request - Failed
  This feature validates that functionality related to commit the create multicast request - Failed

   Scenario Outline: tc_19 : Create the Multicast dry run Success
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    When I validate that the request record should "not-exist" in the table "vpn_service" by "vpn_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  | published                           |  bng_to_portal                                  |
     |tc_19   | _create_multicast_dry_run_success    | _create_multicast_dry_run_bng_to_portal_success  |


#   Scenario Outline: Commit multicast Failed
#    Given "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
#    When "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
#    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "failed" state
#    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "failed" state
#    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
#    When I validate that the request record should "not exist" in the table "vpn_service" by "vpn_id"
#    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG
#
#    Examples:
#     |tc_num | published                                |  bng_to_portal                                           |
#     |tc_19  | _commit_multicast_dry_run_request_failed |  _commit_multicast_dry_run_request_bng_to_portal_failed  |

