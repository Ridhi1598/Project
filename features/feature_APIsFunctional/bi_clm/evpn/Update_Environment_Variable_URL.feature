@evpn @updateEnv @env @preSetup
Feature: Update rate limit environment variable of evpn from OCP deployment config
  This feature updates the environment variable for evpn

 Scenario: Update environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "update" the "URL" variables of the "evpn-svc-controller"
   When Generate command to show all the "initial" variables of the "evpn-svc-controller"
   When Generate command to show all the "changed" variables of the "evpn-svc-controller"
   And Create batch file and execute the commands for "evpn-svc-controller"
   Then Validate that environment variables are successfully changed