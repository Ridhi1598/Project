@tc46 @bngController
Feature: Patch l3vpn dry run request - success
  This feature validates that functionality related to patch the l3vpn dry run request - success

   Scenario Outline: tc_46 : This scenario validate that the functionality related to Patch l3vpn dry run request - success
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    When Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  | published                             |  bng_to_portal                                              |
     |tc_46   | _patch_l3vpn_dry_run_request_success  | _patch_l3vpn_dry_run_request_success_bng_to_portal_success  |


   Scenario Outline: tc_46 : This Scenario validates that functionality related to commit the patch l3vpn dry run request - success
     Given I read the testdata for commit the patch l3vpn dry run request
     When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
     Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "failed" state
     When Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "failed" state
     Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  | published                           | bng_to_portal                                          |
     |tc_46   | _patch_l3vpn_commit_request_failed  |_patch_l3vpn_commit_request_failed_bng_to_portal_failed |
