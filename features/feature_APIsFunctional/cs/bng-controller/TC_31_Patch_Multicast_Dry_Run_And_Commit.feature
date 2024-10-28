@tc31 @bngController
Feature: Patch Multicast dry run and commit - Success
  This feature validates that functionality related to Multicast the dry run and commit the request

   Scenario Outline: tc_31: This scenario validate that the functionality related to patch the multicast dry run failed
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num   | published                        |  bng_to_orchestrator                                 |
     |tc_31   | _patch_multicast_dry_run_success  | _patch_multicast_dry_run_bng_to_orchestrator_success |


   Scenario Outline: tc_31: This scenario validate that the functionality related to patch the Multicast request - failed
    Given I read the testdata for patch commit multicast dry run request
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "in progress" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    Then I validate that the request record should "exist" in the table "vpn_node" by "vpn_id"
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  | published                             | bng_to_orchestrator                                       |
     |tc_31   | _multicast_dry_run_and_commit_success | _multicast_dry_run_and_commit_bng_to_orchestrator_success |

