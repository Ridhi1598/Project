@bng-svc-controller @restoreEnv @env @postSetup
Feature: Restore environment variables of orchestrator from OCP deployment config
  This feature restores the environment variable for orchestrator

 Scenario: Restore Testing environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "restore" the "Environment" variables of the "bng-svc-controller"
   When Generate command to show all the "initial" variables of the "bng-svc-controller"
   When Generate command to show all the "changed" variables of the "bng-svc-controller"
   And Create batch file and execute the commands for "bng-svc-controller"
   Then Validate that environment variables are successfully changed