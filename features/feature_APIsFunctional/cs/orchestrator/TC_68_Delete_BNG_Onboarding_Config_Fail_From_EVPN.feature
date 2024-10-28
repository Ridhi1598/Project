@tc68 @orchestrator
Feature: Delete BNG onboarding config - Fail from EVPN
This feature test the functionality related to delete the BNG onboarding config - Failed

  Scenario: Delete BNG onboarding config - Fail from EVPN
    Given I read test data for CS testcases
    When "Publish" "tc_68_delete_bng_onboarding_config_failed_from_evpn" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    Then "Publish" "tc_68_delete_bng_onboarding_config_bng_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
    When "Publish" "tc_68_delete_bng_onboarding_config_evpn_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_68_delete_bng_onboarding_config_orchestrator_to_portal_failed_from_evpn" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    When I validate that the request record should "exist" in the table "active_bngs" by "bng_clli_group" for orchestrator
    Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "failed" state