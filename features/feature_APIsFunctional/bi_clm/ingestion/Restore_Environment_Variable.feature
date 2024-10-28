@ingestion @restoreEnv @env @postSetup
Feature: Restore environment variables of ingestion from OCP deployment config
  This feature restores the environment variable for ingestion

 Scenario: Restore timeout environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "restore" the "Environment" variables of the "ingestion-service"
   When Generate command to show all the "initial" variables of the "ingestion-service"
   When Generate command to show all the "changed" variables of the "ingestion-service"
   And Create batch file and execute the commands for "ingestion-service"
   Then Validate that environment variables are successfully changed