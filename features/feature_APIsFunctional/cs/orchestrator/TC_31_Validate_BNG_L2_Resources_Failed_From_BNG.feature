@tc31 @orchestrator
Feature: Validate BNG L2 resources - Failed
  This feature test the functionality related to Validate the BNG L2 resources

   Scenario: Validate BNG L2 resources - Failed
    Given I read test data for CS testcases
    When "Publish" "tc_31_validate_bng_l2_resources_failed_from_bng" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    Then "Publish" "tc_31_validate_bng_l2_resources_bng_to_orchestrator_failed_from_bng" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_31_validate_bng_l2_resources_orchestrator_to_portal_failed_from_bng" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator