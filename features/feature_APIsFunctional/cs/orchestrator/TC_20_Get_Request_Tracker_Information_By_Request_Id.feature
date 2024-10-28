@tc20 @orchestrator
Feature: Get request tracker information by request-id
  This feature test the functionality related to get request tracker information by request-id

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

   Scenario: tc_20 : Get request tracker information by requestId
     Given I read test data for orchestrator testcases
     When "Publish" "tc_20_get_request_tracker_info" message to "RMQ" "orchestrator" queue for Orchestrator
     Then "Read" and validate that the "baseRequestId" "tc_20_get_request_tracker_info_orchestrator_to_portal" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
     Then I dump the cs_orchestrator object