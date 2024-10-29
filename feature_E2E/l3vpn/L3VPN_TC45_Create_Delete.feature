@OA2501-1
Feature: TC_45: Create and Delete GRF rip test
  This feature tests the api calls related to creating and deleting a L3VPN Service

Background: Generating access-token
    Given I generate access token for L3VPN

@createL3VPNService @TC_45
Scenario: Create/Update service with valid payload and in valid state
  When I set L3VPN "REST" url
  Then I set api endpoint for testcase "45" for l3vpn
  Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
  And I Set HEADER param request "Authorization" as "access-token" for L3VPN
  And Set request Body for L3VPN
  When Send Http request for L3VPN
  Then I validate the IE response as "completed"
  And I create SSH connection to the device "user"
  When I run "show running-config router rip" command and store the device config
  Then I validate the output of "router_rip" section at "default-level"
  When I run "show running-config interface gigabitethernet 0/1.11" command and store the device config
  Then I validate the output of "interface_gigabitethernet_0/1.11" section at "default-level"
  And I close the SSH connection

@deleteService @TC_105
Scenario: Delete the created service for TC_105 which is in valid state
  When I set L3VPN "REST" url
  Then I set api endpoint for testcase "105" for l3vpn
  And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
  And I Set HEADER param request "Authorization" as "access-token" for L3VPN
  And Set request Body for L3VPN
  When Send Http request for L3VPN
  Then I validate the IE response as "completed"



