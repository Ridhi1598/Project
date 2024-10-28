@tc69 @orchestrator
Feature: Delete BNG onboarding config - Timeout from EVPN
This feature test the functionality related to delete the BNG onboarding config - Timeout

  Scenario: tc_69 : Delete BNG onboarding config - Timeout from EVPN
    Given I read test data for orchestrator testcases
    When "Publish" "tc_69_delete_bng_onboarding_config_timeout_from_evpn" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "tc_69_delete_bng_onboarding_config_l2_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    Then "Publish" "tc_69_delete_olt_onboarding_config_bng_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator
    Then I wait for "350" seconds for request to be timed out
    Then "Read" and validate that the "baseRequestId" "tc_69_delete_bng_onboarding_config_orchestrator_to_portal_timeout_from_evpn" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    When I validate that the request record should "exist" in the table "active_olts" by "clli_name" for orchestrator
