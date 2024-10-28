@ingestionEngine
Feature: Restore timeout environment variable of ingestion engine from OCP deployment config
  This feature restores the environment variable for ingestion engine

 Scenario: Restore timeout environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "restore" the "Environment" variables of the "ingestion-engine"
   When Generate command to show all the "initial" variables of the "ingestion-engine"
   When Generate command to show all the "changed" variables of the "ingestion-engine"
   And Create batch file and execute the commands for "ingestion-engine"
   Then Validate that environment variables are successfully changed