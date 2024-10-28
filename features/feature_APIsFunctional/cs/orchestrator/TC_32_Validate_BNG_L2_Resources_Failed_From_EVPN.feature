@tc32 @orchestrator
Feature: Validate BNG L2 resources Failed from EVPN
  This feature test the functionality related to validate the BNG L2 resources failed from EVPN

   Scenario: Validate BNG L2 resources from EVPN
    Given I read test data for CS testcases
    When "Publish" "tc_32_validate_bng_l2_resources_failed_from_evpn" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator

    Then "Publish" "tc_32_validate_bng_l2_resources_bng_to_orchestrator_failed_from_evpn" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator

    Then "Publish" "tc_32_validate_bng_l2_resources_evpn_to_orchestrator_failed_from_evpn" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_32_validate_bng_l2_resource_orchestrator_to_portal_failed_from_evpn" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator