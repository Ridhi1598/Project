@controller @rmq @updateEnv @env @preSetup @demo
Feature: Update executor host and callback URL of controller
  This feature updates the environment variable for controller

 Scenario: Update environment variables for executor and callback URL
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "URL" variables of the "controller"
   When Generate command to show all the "initial" variables of the "controller"
   When Generate command to show all the "changed" variables of the "controller"
   And Create batch file and execute the commands for "controller"
   Then Validate that environment variables are successfully changed