@util @rmq @updateEnv @env @preSetup
Feature: Update timeout environment variable of controller from OCP deployment config
  This feature updates the environment variable for controller

 Scenario: Update timeout environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "Test" variables of the "utils"
   When Generate command to show all the "initial" variables of the "utils"
   When Generate command to show all the "changed" variables of the "utils"
   And Create batch file and execute the commands for "utils"
   Then Validate that environment variables are successfully changed