@tc10 @bngController
Feature: Commit create bng dry run request - Success
  This feature validates that functionality related to commit the create bng dry run request - Success

   Scenario Outline: tc_10: This scenario validate that the functionality related to create the BNG dry run
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num   | published                  |  bng_to_orchestrator                              |
     |tc_10   | _create_bng_dry_run_success | _create_bng_dry_run_bng_to_orchestrator_success  |


   Scenario Outline: tc_10: This scenario validate that the functionality related to commit create bng dry run request - Failed
    Given "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "failed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "failed" state
    When I validate that the request record should "not-exist" in the table "bng_group" by "bng_group_id"
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num | published                            |  bng_to_orchestrator                                    |
     |tc_10  | _commit_bng_dry_run_request_failed  |  _commit_bng_dry_run_request_bng_to_orchestrator_failed  |

