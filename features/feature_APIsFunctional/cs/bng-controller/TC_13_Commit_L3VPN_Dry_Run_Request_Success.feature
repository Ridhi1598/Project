@tc13 @bngController
Feature: Commit create L3VPN run request - Success
  This feature validates that functionality related to commit the create L3VPN dry run request - Success

   Scenario Outline: tc_7: This scenario validate that the functionality related to create the BNG dry run
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num | published                    |  bng_to_portal                             |
     |tc_7   | _create_bng_dry_run_success  |  _create_bng_dry_run_bng_to_portal_success |


   Scenario Outline: tc_9: This scenario validate that the functionality related to commit create bng dry run request - Success
    Given I read the testdata for commit requests
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG
    When I validate that the request record should "exist" in the table "bng_external_request_tracker" by "parent_request_tracker_id"
    Then I validate the state of requests for the "commit success" scenario in the "bng_external_request_tracker" table using the "id"
    Then Get and verify the "committed" request record by "id" from table "bng_bsaf_request_tracker" with "committed" state

    Examples:
     |tc_num | published                                  | bng_to_portal                             |
     |tc_9   | _commit_bng_dry_run_request_success |_commit_bng_dry_run_request_bng_to_portal_success |


   Scenario Outline: tc_11: This scenario validate that the functionality related to create the L3VPN dry run
    Given I read the testdata for L3VPN dry run testcase
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num   | published                     |  bng_to_portal                                |
     |tc_11   | _create_l3vpn_dry_run_success  |  _create_l3vpn_dry_run_bng_to_portal_success  |


   Scenario Outline: tc_13: This scenario validate that the functionality related to commit create bng dry run request - Success
    Given I read the testdata for commit requests
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG
    When I validate that the request record should "exist" in the table "bng_external_request_tracker" by "parent_request_tracker_id"
    Then I validate the state of requests for the "commit success" scenario in the "bng_external_request_tracker" table using the "id"
    Then Get and verify the "committed" request record by "id" from table "bng_bsaf_request_tracker" with "committed" state

    Examples:
     |tc_num | published                             |  bng_to_portal                                       |
     |tc_13  | _commit_l3vpn_dry_run_request_success | _commit_l3vpn_dry_run_request_bng_to_portal_success |


 Scenario: tc_14: This scenario validate that the functionality related to create Tp Request sent to topology
    Given I validate the L3VPN request record from "bng_external_request_tracker" table using the "parent_request_tracker_id"
    When I validate that the request record should "exist" in the table "bng_external_request_tracker" by "id"
    Then I read test data for BNG controller testcases
    When I validate that the request record should "exist" in the table "vpn_service" by "vpn_id"
    When I validate that the request record should "exist" in the table "vpn_node" by "vpn_id"


