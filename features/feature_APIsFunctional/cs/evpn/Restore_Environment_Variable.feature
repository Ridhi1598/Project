@evpn @rmq @restoreEnv @env @postSetup @demo
Feature: Restore timeout environment variable of controller from OCP deployment config
  This feature restores the environment variable for controller

 Scenario: Restore timeout environment variables
   Given Generate command for ocp login
   Given Generate command to access current working project
   When Generate command to "restore" the "Environment" variables of the "evpn-svc-controller"
   When Generate command to show all the "initial" variables of the "evpn-svc-controller"
   When Generate command to show all the "changed" variables of the "evpn-svc-controller"
   And Create batch file and execute the commands for "evpn-svc-controller"
   Then Validate that environment variables are successfully changed