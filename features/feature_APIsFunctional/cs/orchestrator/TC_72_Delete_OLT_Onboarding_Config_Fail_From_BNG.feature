@tc72 @orchestrator
Feature: Delete OLT onboarding config - Fail from BNG
This feature test the functionality related to delete the OLT onboarding config - Fail from BNG

Scenario: tc_72 : Delete OLT onboarding config - Fail from BNG
  Given I read test data for orchestrator testcases
  When "Publish" "tc_72_delete_olt_onboarding_config_fail_from_bng" message to "RMQ" "orchestrator" queue for Orchestrator
  When "Read" and validate that the "create" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for Orchestrator
  Then "Publish" "tc_72_delete_olt_onboarding_config_l2_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator
  When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
  Then "Publish" "tc_72_delete_olt_onboarding_config_bng_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator
  Then "Read" and validate that the "baseRequestId" "tc_72_delete_olt_onboarding_config_orchestrator_to_portal" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
  Then I validate that the request record should "exist" in the table "active_olts" by "clli_name" for orchestrator
  Then I validate the "created" request record by "id" from table "orch_bsaf_request_tracker" with "failed" state
