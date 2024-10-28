@ASR920-6
Feature: TC_25: Create and update full service VRF
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN
    When I set L3VPN "REST" url

  @createL3VPNService @TC_27
  Scenario: Create/Update service with valid payload and in valid state
    Then I set api endpoint for testcase "27" for L3VPN
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set Header param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    When I query the content of section "interface GigabitEthernet0/0/2" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/2" section
    Then I validate the value of "encapsulation dot1q" section
    When I query the content of section "interface GigabitEthernet0/0/4" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/4" section
    When I query the content of section "interface BDI2561" at "0" level
    Then I validate the output of "interface_BDI2561" section
    When I query the content of section "interface BDI2571" at "0" level
    Then I validate the output of "interface_BDI2571" section
    When I query the content of section "router bgp 65026" at "0" level
    Then I validate the output of "router_bgp_65026" section
    When I query the content of section "policy-map LAN_OUT_VPN2g" at "0" level
    Then I validate the output of "policy-map_LAN_OUT_VPN2g" section
    When I query the content of section "policy-map LAN_OUT" at "0" level
    Then I validate the output of "policy-map_LAN_OUT" section
    When I query the content of section "policy-map WAN_OUT" at "0" level
    Then I validate the output of "policy-map_WAN_OUT" section
    When I query the content of section "policy-map LAN_IN_VPN2g" at "0" level
    Then I validate the output of "policy-map_LAN_IN_VPN2g" section
    When I query the content of section "policy-map WAN_IN_VPN2g" at "0" level
    Then I validate the output of "policy-map_WAN_IN_VPN2g" section
    When I query the content of section "policy-map WAN_IN_MEA" at "0" level
    Then I validate the output of "policy-map_WAN_IN_MEA" section
    When I query the content of section "policy-map PARENT_WAN_OUT" at "0" level
    Then I validate the output of "policy-map_PARENT_WAN_OUT" section
    When I query the content of section "policy-map LAN_IN" at "0" level
    Then I validate the output of "policy-map_LAN_IN" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_EF" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_EF" section
    When I query the content of section "class-map match-any QOS_GROUP_EF" at "0" level
    Then I validate the output of "class-map_match-any_QOS_GROUP_EF" section
    When I query the content of section "class-map match-any LAN_EF" at "0" level
    Then I validate the output of "class-map_match-any_LAN_EF" section
    When I query the content of section "class-map match-any LAN_AF3" at "0" level
    Then I validate the output of "class-map_match-any_LAN_AF3" section
    When I query the content of section "class-map match-any LAN_AF2" at "0" level
    Then I validate the output of "class-map_match-any_LAN_AF2" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_AF1" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_AF1" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_AF3" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_AF3" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_AF2" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_AF2" section
    When I query the content of section "class-map match-any LAN_VPN2g" at "0" level
    Then I validate the output of "class-map_match-any_LAN_VPN2g" section
    When I query the content of section "class-map match-any WAN_VPN2g" at "0" level
    Then I validate the output of "class-map_match-any_WAN_VPN2g" section
    And I close the SSH connection

 @createL3VPNService @TC_28
  Scenario: Create/Update service with valid payload and in valid state
    Then I set api endpoint for testcase "28" for L3VPN
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set Header param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    When I query the content of section "interface GigabitEthernet0/0/2" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/2" section
    Then I validate the value of "encapsulation dot1q" section
    When I query the content of section "interface GigabitEthernet0/0/4" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/4" section
    When I query the content of section "interface BDI2561" at "0" level
    Then I validate the output of "interface_BDI2561" section
    When I query the content of section "interface BDI2571" at "0" level
    Then I validate the output of "interface_BDI2571" section
    When I query the content of section "router bgp 65026" at "0" level
    Then I validate the output of "router_bgp_65026" section
    When I query the content of section "policy-map LAN_OUT_VPN2g" at "0" level
    Then I validate the output of "policy-map_LAN_OUT_VPN2g" section
    When I query the content of section "policy-map LAN_OUT" at "0" level
    Then I validate the output of "policy-map_LAN_OUT" section
    When I query the content of section "policy-map WAN_OUT" at "0" level
    Then I validate the output of "policy-map_WAN_OUT" section
    When I query the content of section "policy-map LAN_IN_VPN2g" at "0" level
    Then I validate the output of "policy-map_LAN_IN_VPN2g" section
    When I query the content of section "policy-map WAN_IN_VPN2g" at "0" level
    Then I validate the output of "policy-map_WAN_IN_VPN2g" section
    When I query the content of section "policy-map WAN_IN_MEA" at "0" level
    Then I validate the output of "policy-map_WAN_IN_MEA" section
    When I query the content of section "policy-map PARENT_WAN_OUT" at "0" level
    Then I validate the output of "policy-map_PARENT_WAN_OUT" section
    When I query the content of section "policy-map LAN_IN" at "0" level
    Then I validate the output of "policy-map_LAN_IN" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_EF" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_EF" section
    When I query the content of section "class-map match-any QOS_GROUP_EF" at "0" level
    Then I validate the output of "class-map_match-any_QOS_GROUP_EF" section
    When I query the content of section "class-map match-any LAN_EF" at "0" level
    Then I validate the output of "class-map_match-any_LAN_EF" section
    When I query the content of section "class-map match-any LAN_AF3" at "0" level
    Then I validate the output of "class-map_match-any_LAN_AF3" section
    When I query the content of section "class-map match-any LAN_AF2" at "0" level
    Then I validate the output of "class-map_match-any_LAN_AF2" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_AF1" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_AF1" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_AF3" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_AF3" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_AF2" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_AF2" section
    When I query the content of section "class-map match-any LAN_VPN2g" at "0" level
    Then I validate the output of "class-map_match-any_LAN_VPN2g" section
    When I query the content of section "class-map match-any WAN_VPN2g" at "0" level
    Then I validate the output of "class-map_match-any_WAN_VPN2g" section
    And I close the SSH connection

 @createL3VPNService @TC_29
  Scenario: Create/Update service with valid payload and in valid state
    Then I set api endpoint for testcase "29" for L3VPN
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set Header param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    When I query the content of section "interface GigabitEthernet0/0/2" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/2" section
    Then I validate the value of "encapsulation dot1q" section
    When I query the content of section "interface GigabitEthernet0/0/4" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/4" section
    When I query the content of section "interface BDI2561" at "0" level
    Then I validate the output of "interface_BDI2561" section
    When I query the content of section "interface BDI2571" at "0" level
    Then I validate the output of "interface_BDI2571" section
    When I query the content of section "router bgp 65026" at "0" level
    Then I validate the output of "router_bgp_65026" section
    When I query the content of section "policy-map LAN_OUT_VPN2g" at "0" level
    Then I validate the output of "policy-map_LAN_OUT_VPN2g" section
    When I query the content of section "policy-map LAN_OUT" at "0" level
    Then I validate the output of "policy-map_LAN_OUT" section
    When I query the content of section "policy-map WAN_OUT" at "0" level
    Then I validate the output of "policy-map_WAN_OUT" section
    When I query the content of section "policy-map LAN_IN_VPN2g" at "0" level
    Then I validate the output of "policy-map_LAN_IN_VPN2g" section
    When I query the content of section "policy-map WAN_IN_VPN2g" at "0" level
    Then I validate the output of "policy-map_WAN_IN_VPN2g" section
    When I query the content of section "policy-map WAN_IN_MEA" at "0" level
    Then I validate the output of "policy-map_WAN_IN_MEA" section
    When I query the content of section "policy-map PARENT_WAN_OUT" at "0" level
    Then I validate the output of "policy-map_PARENT_WAN_OUT" section
    When I query the content of section "policy-map LAN_IN" at "0" level
    Then I validate the output of "policy-map_LAN_IN" section
    When I query the content of section "class-map match-any QOS_GROUP_EF" at "0" level
    Then I validate the output of "class-map_match-any_QOS_GROUP_EF" section
    When I query the content of section "class-map match-any LAN_EF" at "0" level
    Then I validate the output of "class-map_match-any_LAN_EF" section
    When I query the content of section "class-map match-any LAN_AF3" at "0" level
    Then I validate the output of "class-map_match-any_LAN_AF3" section
    When I query the content of section "class-map match-any LAN_AF2" at "0" level
    Then I validate the output of "class-map_match-any_LAN_AF2" section
    When I query the content of section "class-map match-any LAN_VPN2g" at "0" level
    Then I validate the output of "class-map_match-any_LAN_VPN2g" section
    When I query the content of section "class-map match-any WAN_VPN2g" at "0" level
    Then I validate the output of "class-map_match-any_WAN_VPN2g" section
    And I close the SSH connection

  @deleteService @TC_87
  Scenario:Delete the created service for TC_87 which is in valid state
    When I set api endpoint for testcase "87" for L3VPN
    Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"