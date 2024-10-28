@cs-polling-engine @updateEnv @env @preSetup
Feature: Update rate limit environment variable of cs-polling-engine from OCP deployment config
  This feature updates the environment variable for cs-polling-engine

 Scenario: Update Testing environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "Environment" variables of the "cs-polling-engine"
   When Generate command to show all the "initial" variables of the "cs-polling-engine"
   When Generate command to show all the "changed" variables of the "cs-polling-engine"
   And Create batch file and execute the commands for "cs-polling-engine"
   Then Validate that environment variables are successfully changed