@ASR920-6
Feature: TC_23: Create and Delete QPV VRF service
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_23
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "23" for L3VPN
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
    When I query the content of section "policy-map LAN_OUT_VPN2_asr6" at "0" level
    Then I validate the output of "policy-map_LAN_OUT_VPN2_asr6" section
    When I query the content of section "policy-map WAN_OUT_VPN2_asr6" at "0" level
    Then I validate the output of "policy-map_WAN_OUT_VPN2_asr6" section
    When I query the content of section "policy-map WAN_IN_VPN2_asr6" at "0" level
    Then I validate the output of "policy-map_WAN_IN_VPN2_asr6" section
    When I query the content of section "policy-map WAN_IN_MEA" at "0" level
    Then I validate the output of "policy-map_WAN_IN_MEA" section
    When I query the content of section "policy-map WAN_OUT_PER_VPN" at "0" level
    Then I validate the output of "policy-map_WAN_OUT_PER_VPN" section
    When I query the content of section "policy-map LAN_IN_VPN2_asr6" at "0" level
    Then I validate the output of "policy-map_LAN_IN_VPN2_asr6" section
    When I query the content of section "policy-map LAN_IN" at "0" level
    Then I validate the output of "policy-map_LAN_IN" section
    When I query the content of section "class-map match-all LAN_QOS_GROUP_EF" at "0" level
    Then I validate the output of "class-map_match-all_LAN_QOS_GROUP_EF" section
    When I query the content of section "class-map match-any QOS_GROUP_EF" at "0" level
    Then I validate the output of "class-map_match-any_QOS_GROUP_EF" section
#    When I query the content of section "class-map match-any QOS_GROUPS" at "0" level
#    Then I validate the output of "class-map_match-any_QOS_GROUPS" section
    When I query the content of section "class-map match-any LAN_EF" at "0" level
    Then I validate the output of "class-map_match-any_LAN_EF" section
#    When I query the content of section "class-map match-any QOS_GROUP_AF1" at "0" level
#    Then I validate the output of "class-map_match-any_QOS_GROUP_AF1" section
#    When I query the content of section "class-map match-any QOS_GROUP_AF3" at "0" level
#    Then I validate the output of "class-map_match-any_QOS_GROUP_AF3" section
#    When I query the content of section "class-map match-any QOS_GROUP_AF2" at "0" level
#    Then I validate the output of "class-map_match-any_QOS_GROUP_AF2" section
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
    When I query the content of section "class-map match-any LAN_VPN2_asr6" at "0" level
    Then I validate the output of "class-map_match-any_LAN_VPN2_asr6" section
    When I query the content of section "class-map match-any WAN_VPN2_asr6" at "0" level
    Then I validate the output of "class-map_match-any_WAN_VPN2_asr6" section
    And I close the SSH connection

  @deleteService @TC_83
  Scenario:Delete the created service for TC_83 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "83" for L3VPN
    Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"