@tc64 @orchestrator
Feature: Push OLT onboarding config - Fail from EVPN cont
  This feature validates that functionality related to unlock the BNG l2-resources


  Scenario: tc_14 :Create the OLT onboarding config
    Given I read test data for orchestrator testcases
    When "Publish" "tc_14_create_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
    Then "Publish" "tc_14_create_olt_onboarding_config_l2_to_orchestrator_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
    Then "Publish" "tc_14_create_olt_onboarding_config_evpn_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    Then "Publish" "tc_14_create_olt_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "second" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
    Then "Publish" "tc_14_create_olt_onboarding_config_evpn_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
    When "Read" and validate that the "second" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
    Then "Publish" "tc_14_create_olt_onboarding_config_bng_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_14_create_olt_onboarding_config_orchestrator_to_portal_success" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

  Scenario: TC 64 Push OLT onboarding config - Fail from EVPN cont
    Given I read test data for CS testcases
    When "Publish" "tc_16_push_olt_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
    Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "in progress" state
    Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
    When "Publish" "tc_64_evpn_to_orchestrator_first_request_failed" message to "RMQ" "orchestrator" queue for Orchestrator
    Then "Read" and validate that the "baseRequestId" "tc_64_push_olt_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
    Then I validate that the request record should "not-exist" in the table "active_olts" by "clli_name" for orchestrator
    Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "failed" state
    Then I dump the cs_orchestrator object