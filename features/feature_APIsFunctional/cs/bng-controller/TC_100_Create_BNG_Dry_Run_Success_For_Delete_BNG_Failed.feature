@tc100 @bngController
Feature: Create the bng dry run success for delete bng failed
  This feature validates that functionality related to create the bng dry run success for delete bng failed

   Scenario Outline: tc_100: This scenario validate that the functionality related to create the bng dry run success for delete bng failed
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state

    Examples:
     |tc_num    | published                                        |
     |tc_100   | _create_bng_dry_run_success_for_delete_bng_failed |


   Scenario Outline: tc_101 :This scenario validate that the functionality related to commit the bng dry run success for delete bng failed
    Given "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    Then I validate that the request record should "exist" in the table "bng_external_request_tracker" by "parent_request_tracker_id"
    Then I validate the state of requests for the "commit success" scenario in the "bng_external_request_tracker" table using the "id"


    Examples:
     |tc_num    | published                                        |
     |tc_101   | _commit_bng_dry_run_success_for_delete_bng_failed |


   Scenario Outline: tc_102: This scenario validate that the functionality related to create the L3VPN dry run for delete L3VPN dry run failed
    Given I read the testdata for L3VPN dry run testcase
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"

    Examples:
     |tc_num   | published                                                      |
     |tc_102   | _create_l3vpn_dry_run_success_for_delete_l3vpn_dry_run_failed  |


   Scenario Outline: tc_103: This scenario validate that the functionality related to commit create bng dry run request - Success
    Given I read the testdata for commit requests
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    When I validate that the request record should "exist" in the table "bng_external_request_tracker" by "parent_request_tracker_id"
    Then I validate the state of requests for the "commit success" scenario in the "bng_external_request_tracker" table using the "id"
    Then Get and verify the "committed" request record by "id" from table "bng_bsaf_request_tracker" with "committed" state

    Examples:
     |tc_num   | published                                                             |
     |tc_103  | _commit_l3vpn_dry_run_request_success_for_failed_delete_l3vpn_dry_run  |


 Scenario: tc_104: This scenario validate that the functionality related to create Tp Request sent to topology for_delete_l3vpn_dry_run
    Given I validate the L3VPN request record from "bng_external_request_tracker" table using the "parent_request_tracker_id"
    When I validate that the request record should "exist" in the table "bng_external_request_tracker" by "id"
    Then I read test data for BNG controller testcases
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for commit requests

