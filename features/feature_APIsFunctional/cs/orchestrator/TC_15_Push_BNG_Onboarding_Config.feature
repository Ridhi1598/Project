@tc15 @orchestrator
Feature: Push BNG onboarding config
  This feature test the functionality related to push the BNG onboarding config

   Scenario: tc_13 : Create the BNG onboarding config
     Given I read test data for orchestrator testcases
     When "Publish" "tc_13_create_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "in progress" state
     Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     When "Publish" "tc_13_create_bng_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     When "Publish" "tc_13_create_bng_onboarding_config_evpn_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "second" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     When "Publish" "tc_13_create_bng_onboarding_config_bng_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_13_create_bng_onboarding_config_orchestrator_to_portal_success" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
     Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "completed" state

   Scenario: tc_15: Push BNG onboarding config
     Given I read test data for orchestrator testcases
     When "Publish" "tc_15_push_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "in progress" state
     When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     Then "Publish" "tc_15_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     When "Publish" "tc_15_evpn_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "second" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     Then "Publish" "tc_15_bng_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "baseRequestId" "tc_15_orchestrator_to_portal_success" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
     Then I validate that the request record should "exist" in the table "active_bngs" by "bng_clli_group" for orchestrator
     Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "completed" state
     Then I dump the cs_orchestrator object