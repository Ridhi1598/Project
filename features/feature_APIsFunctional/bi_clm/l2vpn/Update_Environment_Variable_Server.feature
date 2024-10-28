@l3vpn @updateEnv @env @preSetup
Feature: Update rate limit environment variable of l2vpn controller from OCP deployment config
  This feature updates the environment variable for l2vpn controller

 Scenario: Update Server environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "Server" variables of the "l2vpn-svc-controller"
   When Generate command to show all the "initial" variables of the "l2vpn-svc-controller"
   When Generate command to show all the "changed" variables of the "l2vpn-svc-controller"
   And Create batch file and execute the commands for "l2vpn-svc-controller"
   Then Validate that environment variables are successfully changed