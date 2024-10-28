@tc57 @orchestrator
  Feature: Push BNG onboarding config - Fail from BNG
  This feature test the functionality related to push the BNG onboarding config - Fail from BNG

   Scenario: tc_13 : Create the BNG onboarding config
     Given I read test data for orchestrator testcases
     When "Publish" "tc_13_create_bng_onboarding_config_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     When "Publish" "tc_13_create_bng_onboarding_config_bng_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "create" "evpn_request" message is published in the "RMQ" "evpn_controller_test" queue for Orchestrator
     When "Publish" "tc_13_create_bng_onboarding_config_evpn_to_orchestrator_first_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "second" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     When "Publish" "tc_13_create_bng_onboarding_config_bng_to_orchestrator_second_request_success" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_13_create_bng_onboarding_config_orchestrator_to_portal_success" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator

   Scenario: tc_57 : Push BNG onboarding config - Fail from BNG
    Given I read test data for orchestrator testcases
     When "Publish" "tc_57_push_bng_onboarding_config_fail_from_bng" message to "RMQ" "orchestrator" queue for Orchestrator
     When "Read" and validate that the "create" "bng_request" message is published in the "RMQ" "bng_controller_test" queue for Orchestrator
     Then "Publish" "tc_57_bng_to_orchestrator_first_request" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_57_create_olt_onboarding_config_orchestrator_to_portal_fail_from_bng" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
