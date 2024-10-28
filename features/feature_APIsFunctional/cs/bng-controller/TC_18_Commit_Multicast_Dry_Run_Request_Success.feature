@tc18 @bngController
Feature: Commit create Multicast dry run request - Success
  This feature validates that functionality related to commit the create multicast dry run request - Success

   Scenario Outline: tc_16 : This scenario validate that the functionality related to create the Multicast dry run - Success
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  | published                           |  bng_to_orchestrator                              |
     |tc_16   | _create_multicast_dry_run_success   |  _create_multicast_dry_run_bng_to_portal_success |


   Scenario Outline: tc_18 :This scenario validate that the functionality related to commit create multicast dry run request - Success
    Given "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "completed" state
    When I validate that the request record should "exist" in the table "vpn_service" by "vpn_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG
    When I validate that the request record should "exist" in the table "bng_external_request_tracker" by "parent_request_tracker_id"
    Then I validate the state of requests for the "commit success" scenario in the "bng_external_request_tracker" table using the "id"
    Then Get and verify the "committed" request record by "id" from table "bng_bsaf_request_tracker" with "committed" state

    Examples:
     |tc_num | published                                 |  bng_to_orchestrator                                    |
     |tc_18  | _commit_multicast_dry_run_request_success | _commit_multicast_dry_run_request_bng_to_portal_success |

