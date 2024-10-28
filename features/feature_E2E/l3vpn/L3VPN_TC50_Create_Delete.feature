@OA2501-1
Feature: TC_50: Create and Delete
  This feature tests the api calls related to creating and deleting a L3VPN Service

Background: Generating access-token
    Given I generate access token for L3VPN

@createL3VPNService @TC_50
Scenario: Create/Update service with valid payload and in valid state
  When I set L3VPN "REST" url
  Then I set api endpoint for testcase "50" for l3vpn
  Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
  And I Set HEADER param request "Authorization" as "access-token" for L3VPN
  And Set request Body for L3VPN
  When Send Http request for L3VPN
  Then I validate the IE response as "completed"
  And I create SSH connection to the device "user"
  When I run "show running-config ip as-path access-list 11 permit ^852$" command and store the device config
  Then I validate the output of "ip_as-path_access-list_11_permit_^852$" section at "default-level"
  When I run "show running-config ip as-path access-list 11 permit _1691$" command and store the device config
  Then I validate the output of "ip_as-path_access-list_11_permit__1691$" section at "default-level"
  When I run "show running-config ip as-path access-list 11 permit _65013$" command and store the device config
  Then I validate the output of "ip_as-path_access-list_11_permit__65013$" section at "default-level"
  When I run "show running-config ip prefix-list" command and store the device config
  Then I validate the output of "ip_prefix-list" section at "default-level"
  When I run "show running-config ip access-list standard 10" command and store the device config
  Then I validate the output of "ip_access-list_standard 10" section at "default-level"
  When I run "show running-config route-map" command and store the device config
  Then I validate the output of "route-map_BGP_TO_OSPF_deny_20" section at "default-level"
  Then I validate the output of "route-map_BGP_TO_OSPF_deny_30" section at "default-level"
  Then I validate the output of "route-map_BGP_TO_OSPF_deny_40" section at "default-level"
  And I close the SSH connection

@deleteService @TC_110
Scenario: Delete the created service for TC_110 which is in valid state
  When I set L3VPN "REST" url
  Then I set api endpoint for testcase "110" for l3vpn
  And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
  And I Set HEADER param request "Authorization" as "access-token" for L3VPN
  And Set request Body for L3VPN
  When Send Http request for L3VPN
  Then I validate the IE response as "completed"