@ingestion @updateEnv @env @preSetup
Feature: Update timeout environment variable of ingestion from OCP deployment config
  This feature updates the environment variable for ingestion

 Scenario: Update Timeout environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "Timeout" variables of the "ingestion-service"
   When Generate command to show all the "initial" variables of the "ingestion-service"
   When Generate command to show all the "changed" variables of the "ingestion-service"
   And Create batch file and execute the commands for "ingestion-service"
   Then Validate that environment variables are successfully changed