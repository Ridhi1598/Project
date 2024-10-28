@tc18 @orchestrator
Feature: Delete BNG on-boarding config
This feature test the functionality related to delete the BNG on-boarding config

Scenario: Delete BNG on-boarding config
  Given I read test data for CS testcases
  When "Publish" "tc_18_delete_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
  Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "in progress" state
  When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
  Then "Publish" "tc_18_delete_bng_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
  Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
  When "Publish" "tc_18_delete_bng_onboarding_config_evpn_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
  When "Read" and validate that the "second" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
  Then "Publish" "tc_18_delete_bng_onboarding_config_bng_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
  Then "Read" and validate that the "baseRequestId" "tc_18_delete_bng_onboarding_config_orchestrator_to_portal_success" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
  Then I validate that the request record should "not exist" in the table "active_bngs" by "bng_clli_group" for orchestrator
  Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "completed" state