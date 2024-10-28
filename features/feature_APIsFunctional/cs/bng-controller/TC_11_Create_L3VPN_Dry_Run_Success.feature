@tc11 @bngController
Feature: Create the L3VPN dry run
  This feature validates that functionality related to create the L3VPN dry run

   Scenario Outline: tc_11: This scenario validate that the functionality related to create the L3VPN dry run
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num   | published                     |  bng_to_portal                                |
     |tc_11   | _create_l3vpn_dry_run_success  |  _create_l3vpn_dry_run_bng_to_portal_success  |

