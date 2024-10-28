@tc15 @bngController
Feature: Create L3VPN dry run request - Failed
  This feature validates that functionality related to commit the create L3VPN dry run request - Success

   Scenario Outline: tc_15: create the BNG dry run Success
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num | published                     |  bng_to_portal                              |
     |tc_15   | _create_bng_dry_run_success  |  _create_bng_dry_run_bng_to_portal_success  |


   Scenario Outline: tc_15: commit create bng Success
    Given I read the testdata for commit requests
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"


    Examples:
     |tc_num  | published                            | bng_to_portal                                    |
     |tc_15   | _commit_bng_dry_run_request_success  |_commit_bng_dry_run_request_bng_to_portal_success |


   Scenario Outline: tc_15: create the L3VPN dry run Success
    Given I read the testdata for L3VPN dry run testcase
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num   | published                      |  bng_to_portal                                |
     |tc_15    | _create_l3vpn_dry_run_success  |  _create_l3vpn_dry_run_bng_to_portal_success  |


    Scenario Outline: tc_15: create the L3VPN Commit Failed
    Given I read the testdata for commit requests
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "failed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "failed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    When I validate that the request record should "not-exist" in the table "vpn_service" by "vpn_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG
    Then Get and verify the "committed" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state

    Examples:
     |tc_num | published                             |  bng_to_portal                                       |
     |tc_15  | _commit_l3vpn_dry_run_request_failed  | _commit_l3vpn_dry_run_request_bng_to_portal_failed |
    
    Scenario Outline: tc_15: delete bng Success
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "not exist" in the table "bng_group" by "bng_group_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num | published                    |  bng_to_portal                           |
     |tc_15   | _delete_bng_group_success   |  _delete_bng_group_bng_to_portal_success |
