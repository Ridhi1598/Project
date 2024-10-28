@tc45 @orchestrator
Feature: Create BNG onboarding config - Timeout from BNG cont
  This feature test the functionality related to create the BNG onboarding config

   Scenario: TC 45 Create BNG onboarding config - Timeout from BNG cont
     Given I read test data for CS testcases
     When "Publish" "tc_45_create_bng_onboarding_config_timeout" message to "RMQ" "orchestrator" queue for Orchestrator
     Then I wait for "320" seconds for request to be timed out
     Then "Read" and validate that the "baseRequestId" "tc_45_create_bng_onboarding_config_orchestrator_to_portal_failed" message is published in the "RMQ" "cs_portal_test" queue for Orchestrator
