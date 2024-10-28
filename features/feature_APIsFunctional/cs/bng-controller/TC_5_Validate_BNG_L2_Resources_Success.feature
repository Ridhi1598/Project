@tc5 @bngController
Feature: Validate BNG L2 resources
  This feature validates that functionality related to Validate BNG L2 resources - success

   Scenario Outline: tc_5: This scenario validates that the functionality related to validate the BNG L2 resources
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    Then "Read" and validate that the "publishedRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  |  published                  | bng_to_orchestrator        |
     |tc_5    | _validate_bng_l2_resources  | _callback_response         |


