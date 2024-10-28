@controller @rmq @updateEnv @env @preSetup
Feature: Update rate limit environment variable of controller from OCP deployment config
  This feature updates the environment variable for controller

 Scenario: Update Rate Limit environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "RateLimit" variables of the "controller"
   When Generate command to show all the "initial" variables of the "controller"
   When Generate command to show all the "changed" variables of the "controller"
   And Create batch file and execute the commands for "controller"
   Then Validate that environment variables are successfully changed