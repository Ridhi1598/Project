@ASR920-6
Feature: TC_34: Create routing policy bgp to ospf
This feature tests the api calls related to creating and deleting a L3VPN Service

Background: Generating access-token
    Given I generate access token for L3VPN

@createL3VPNService @TC_34
Scenario: Create/Update service with valid payload and in valid state
  When I set L3VPN "REST" url
  Then I set api endpoint for testcase "34" for L3VPN
  And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
  And I set Header param request "Authorization" as "access-token" for L3VPN
  And Set request Body for L3VPN
  When Send Http request for L3VPN
  Then I validate the IE response as "completed"
  When I create SSH connection to the device "user"
  Then I run "show running-config" command and store the device config
  When I validate the show running config output by query "ip_community-list_expanded_MATCH_OSS_permit_1691"
  Then I validate the show running config output by query "ip_as-path_access-list_11_permit_852"
  Then I validate the show running config output by query "ip_as-path_access-list_11_permit_1691"
  Then I validate the show running config output by query "ip_as-path_access-list_11_permit_65013"
  Then I validate the show running config output by query "route-map_BGP_TO_OSPF_deny_10"
  When I query the content of section "router bgp 65026" at "0" level
  Then I validate the output of "router_bgp_65026" section
  And I close the SSH connection

#@deleteService @TC_94
#Scenario:Delete the created service for TC_94 which is in valid state
#  When I set L3VPN "REST" url
#  Then I set api endpoint for testcase "94" for L3VPN
#  Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
#  And I set HEADER param request "Authorization" as "access-token" for L3VPN
#  And Set request Body for L3VPN
#  When Send Http request for L3VPN
#  Then I validate the IE response as "completed"