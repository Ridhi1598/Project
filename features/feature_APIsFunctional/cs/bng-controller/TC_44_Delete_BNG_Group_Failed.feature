@tc44 @bngController
Feature: Delete the BNG group - Failed
  This feature validates that functionality related to delete the BNG dry run

   Scenario Outline: tc_44 : This scenario validate that the functionality related to delete the BNG dry run - Failed
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "failed" state
    Then Get and verify the "created" request record by "parent_request_tracker_id" from table "bng_external_request_tracker" with "failed" state
    When I validate that the request record should "exist" in the table "bng_group" by "bng_group_id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num | published                    |  bng_to_portal                           |
     |tc_44   | _delete_bng_group_failed    |  _delete_bng_group_bng_to_portal_failed  |


