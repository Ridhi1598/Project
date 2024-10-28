@orchestrator @restoreEnv @env @postSetup
Feature: Restore environment variables of orchestrator from OCP deployment config
  This feature restores the environment variable for orchestrator

 Scenario: Restore Testing environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "restore" the "Environment" variables of the "service-orchestrator"
   When Generate command to show all the "initial" variables of the "service-orchestrator"
   When Generate command to show all the "changed" variables of the "service-orchestrator"
   And Create batch file and execute the commands for "service-orchestrator"
   Then Validate that environment variables are successfully changed