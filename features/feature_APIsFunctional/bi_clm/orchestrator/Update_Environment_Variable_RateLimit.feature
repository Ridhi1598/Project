@orchestrator @updateEnv @env @preSetup
Feature: Update rate limit environment variable of orchestrator from OCP deployment config
  This feature updates the environment variable for orchestrator

 Scenario: Update RateLimit environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "RateLimit" variables of the "service-orchestrator"
   When Generate command to show all the "initial" variables of the "service-orchestrator"
   When Generate command to show all the "changed" variables of the "service-orchestrator"
   And Create batch file and execute the commands for "service-orchestrator"
   Then Validate that environment variables are successfully changed