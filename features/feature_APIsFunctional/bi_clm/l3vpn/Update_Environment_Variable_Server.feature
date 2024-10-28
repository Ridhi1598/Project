@l3vpn @updateEnv @env @preSetup
Feature: Update rate limit environment variable of l3vpn controller from OCP deployment config
  This feature updates the environment variable for l3vpn controller

 Scenario: Update Server environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "Server" variables of the "l3vpn-controller"
   When Generate command to show all the "initial" variables of the "l3vpn-controller"
   When Generate command to show all the "changed" variables of the "l3vpn-controller"
   And Create batch file and execute the commands for "l3vpn-controller"
   Then Validate that environment variables are successfully changed