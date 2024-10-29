@OA2501-1
Feature: TC_44: Create and Delete VRF QPV test
  This feature tests the api calls related to creating and deleting a L3VPN Service

Background: Generating access-token
    Given I generate access token for L3VPN

@createL3VPNService @TC_44
Scenario: Create/Update service with valid payload and in valid state
  When I set L3VPN "REST" url
  Then I set api endpoint for testcase "44" for l3vpn
  Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
  And I Set HEADER param request "Authorization" as "access-token" for L3VPN
  And Set request Body for L3VPN
  When Send Http request for L3VPN
  Then I validate the IE response as "completed"
  And I create SSH connection to the device "user"
  When I run "show running-config policy-map WAN_OUT_VPN2_OA" command and store the device config
  Then I validate the output of "policy-map_WAN_OUT_VPN2_OA" section at "default-level"
  When I run "show running-config policy-map WAN_OUT_PER_VPN" command and store the device config
  Then I validate the output of "policy-map_WAN_OUT_PER_VPN" section at "default-level"
  When I run "show running-config policy-map WAN_IN_VPN2_OA" command and store the device config
  Then I validate the output of "policy-map_WAN_IN_VPN2_OA" section at "default-level"
  When I run "show running-config policy-map WAN_IN_MEA" command and store the device config
  Then I validate the output of "policy-map_WAN_IN_MEA" section at "default-level"
  When I run "show running-config policy-map LAN_IN_VPN2_OA" command and store the device config
  Then I validate the output of "policy-map_LAN_IN_VPN2_OA" section at "default-level"
  When I run "show running-config policy-map LAN_IN" command and store the device config
  Then I validate the output of "policy-map_LAN_IN" section at "default-level"
  When I run "show running-config policy-map LAN_OUT_VPN2_OA" command and store the device config
  Then I validate the output of "policy-map_LAN_OUT_VPN2_OA" section at "default-level"
  When I run "show running-config policy-map LAN_OUT" command and store the device config
  Then I validate the output of "policy-map_LAN_OUT" section at "default-level"
  When I run "show running-config class-map LAN_VPN2_OA" command and store the device config
  Then I validate the output of "class-map_match-any_LAN_VPN2_OA" section at "default-level"
  When I run "show running-config class-map LAN_QOS_GROUP_AF1" command and store the device config
  Then I validate the output of "class-map_LAN_QOS_GROUP_AF1" section at "default-level"
  When I run "show running-config class-map LAN_QOS_GROUP_AF2" command and store the device config
  Then I validate the output of "class-map_LAN_QOS_GROUP_AF2" section at "default-level"
  When I run "show running-config class-map LAN_AF2" command and store the device config
  Then I validate the output of "class-map_match-any_LAN_AF2" section at "default-level"
  When I run "show running-config class-map LAN_QOS_GROUP_AF3" command and store the device config
  Then I validate the output of "class-map_LAN_QOS_GROUP_AF3" section at "default-level"
  When I run "show running-config class-map LAN_AF3" command and store the device config
  Then I validate the output of "class-map_match-any_LAN_AF3" section at "default-level"
  When I run "show running-config class-map LAN_QOS_GROUP_EF" command and store the device config
  Then I validate the output of "class-map_LAN_QOS_GROUP_EF" section at "default-level"
  When I run "show running-config class-map LAN_EF" command and store the device config
  Then I validate the output of "class-map_match-any_LAN_EF" section at "default-level"
  When I run "show running-config class-map ANY" command and store the device config
  Then I validate the output of "class-map_ANY" section at "default-level"
  When I run "show running-config class-map WAN_MANAGEMENT" command and store the device config
  Then I validate the output of "class-map_WAN_MANAGEMENT" section at "default-level"
  When I run "show running-config class-map WAN_ROUTING" command and store the device config
  Then I validate the output of "class-map_WAN_ROUTING" section at "default-level"
  When I run "show running-config class-map WAN_VPN2_OA" command and store the device config
  Then I validate the output of "class-map_match-any_WAN_VPN2_OA" section at "default-level"
  When I run "show running-config class-map QOS_GROUP_AF1" command and store the device config
  Then I validate the output of "class-map_QOS_GROUP_AF1" section at "default-level"
  When I run "show running-config class-map QOS_GROUP_AF2" command and store the device config
  Then I validate the output of "class-map_QOS_GROUP_AF2" section at "default-level"
  When I run "show running-config class-map QOS_GROUP_AF3" command and store the device config
  Then I validate the output of "class-map_QOS_GROUP_AF3" section at "default-level"
  When I run "show running-config class-map QOS_GROUP_EF" command and store the device config
  Then I validate the output of "class-map_QOS_GROUP_EF" section at "default-level"
  When I run "show running-config interface gigabitethernet 0/1" command and store the device config
  Then I validate the output of "interface_gigabitethernet_0/1" section at "default-level"
  When I run "show running-config interface gigabitethernet 1/0" command and store the device config
  Then I validate the output of "interface_gigabitethernet_1/0" section at "default-level"
  And I close the SSH connection


@deleteService @TC_104
Scenario: Delete the created service for TC_104 which is in valid state
  When I set L3VPN "REST" url
  Then I set api endpoint for testcase "104" for l3vpn
  And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
  And I Set HEADER param request "Authorization" as "access-token" for L3VPN
  And Set request Body for L3VPN
  When Send Http request for L3VPN
  Then I validate the IE response as "completed"



