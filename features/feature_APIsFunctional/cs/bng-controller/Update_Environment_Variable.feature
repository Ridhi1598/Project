@bng-svc-controller @updateEnv @env @preSetup
Feature: Update rate limit environment variable of orchestrator from OCP deployment config
  This feature updates the environment variable for orchestrator

 Scenario: Update Testing environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "Environment" variables of the "bng-svc-controller"
   When Generate command to show all the "initial" variables of the "bng-svc-controller"
   When Generate command to show all the "changed" variables of the "bng-svc-controller"
   And Create batch file and execute the commands for "bng-svc-controller"
   Then Validate that environment variables are successfully changed