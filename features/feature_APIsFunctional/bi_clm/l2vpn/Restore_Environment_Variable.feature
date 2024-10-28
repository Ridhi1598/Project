@l3vpn @restoreEnv @env @postSetup
Feature: Restore environment variables of l3vpn controller from OCP deployment config
  This feature restores the environment variable for l3vpn controller

 Scenario: Restore environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "restore" the "Environment" variables of the "l2vpn-svc-controller"
   When Generate command to show all the "initial" variables of the "l2vpn-svc-controller"
   When Generate command to show all the "changed" variables of the "l2vpn-svc-controller"
   And Create batch file and execute the commands for "l2vpn-svc-controller"
   Then Validate that environment variables are successfully changed