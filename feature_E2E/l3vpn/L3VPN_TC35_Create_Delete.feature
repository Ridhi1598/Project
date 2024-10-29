@ASR920-6
Feature: TC_35: Create routing policy ospf to bgp
This feature tests the api calls related to creating and deleting a L3VPN Service

Background: Generating access-token
    Given I generate access token for L3VPN

@createL3VPNService @TC_35
Scenario: Create/Update service with valid payload and in valid state
  When I set L3VPN "REST" url
  Then I set api endpoint for testcase "35" for L3VPN
  And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
  And I set Header param request "Authorization" as "access-token" for L3VPN
  And Set request Body for L3VPN
  When Send Http request for L3VPN
  Then I validate the IE response as "completed"
  When I create SSH connection to the device "user"
  Then I run "show running-config | s ospf" command and store the device config
  Then I validate the output of "router_ospfv3" section
  Then I validate the output of "router_ospf" section
  Then I run "show running-config" command and store the device config
  Then I validate the show running config output by query "route-map_OSPF_TO_BGP_deny 10"
  And I close the SSH connection

#@deleteService @TC_95
#Scenario:Delete the created service for TC_95 which is in valid state
#  When I set L3VPN "REST" url
#  Then I set api endpoint for testcase "95" for L3VPN
#  Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
#  And I set HEADER param request "Authorization" as "access-token" for L3VPN
#  And Set request Body for L3VPN
#  When Send Http request for L3VPN
#  Then I validate the IE response as "completed"