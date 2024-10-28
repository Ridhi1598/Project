@tc28 @bngController
Feature: Patch Multicast Dry run - failed
  This feature validates that functionality related to patch the multicast dry run failed

   Scenario Outline: tc_28: This scenario validate that the functionality related to patch the multicast dry run failed
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "failed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "failed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num   | published                       |  bng_to_orchestrator                                  |
     |tc_28   | _patch_multicast_dry_run_failed  |  _patch_multicast_dry_run_bng_to_orchestrator_failed |

