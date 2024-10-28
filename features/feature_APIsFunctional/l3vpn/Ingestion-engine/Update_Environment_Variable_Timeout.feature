@ingestionEngine
Feature: Update timeout environment variable of ingestion engine from OCP deployment config
  This feature updates the environment variable for ingestion engine

 Scenario: Update timeout environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "Timeout" variables of the "ingestion-engine"
   When Generate command to show all the "initial" variables of the "ingestion-engine"
   When Generate command to show all the "changed" variables of the "ingestion-engine"
   And Create batch file and execute the commands for "ingestion-engine"
   Then Validate that environment variables are successfully changed