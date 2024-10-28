@tc45 @bngController
Feature: Patch l3vpn dry run request - Failed
  This feature validates that functionality related to patch l3vpn dry run request - failed

   Scenario Outline: tc_45 : This scenario validate that the functionality related to patch l3vpn dry run request - failed
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "failed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "failed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  | published                            |  bng_to_portal                                   |
     |tc_45   | _patch_l3vpn_dry_run_request_failed  | _patch_l3vpn_dry_run_request_bng_to_portal_failed|
