@ISR_4221_2
Feature: TC_13: Create and Delete GRF and VRF full service QPA test
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_9
  Scenario: Create/Update service with valid payload and in valid state with
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "9" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

  @createL3VPNService @TC_10
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "10" for l3vpn
    When I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

  @createL3VPNService @TC_13
  Scenario: Create and Delete GRF and VRF full service QPA test
    Given I set L3VPN "REST" url
    When I set api endpoint for testcase "13" for l3vpn
    Then Set request Body for L3VPN
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    When I query the content of section "policy-map LAN_OUT_Global" at "0" level
    Then I validate the output of "policy-map_LAN_OUT_Global" section
    When I query the content of section "policy-map LAN_OUT_TEST_VPN2" at "0" level
    Then I validate the output of "policy-map_LAN_OUT_TEST_VPN2" section
    When I query the content of section "policy-map LAN_OUT" at "0" level
    Then I validate the output of "policy-map_LAN_OUT" section
    When I query the content of section "policy-map WAN_IN_TEST_VPN2" at "0" level
    Then I validate the output of "policy-map_WAN_IN_TEST_VPN2" section
    When I query the content of section "policy-map WAN_IN_Global" at "0" level
    Then I validate the output of "policy-map_WAN_IN_Global" section
    When I query the content of section "policy-map WAN_OUT" at "0" level
    Then I validate the output of "policy-map_WAN_OUT" section
    When I query the content of section "policy-map WAN_IN_MEA" at "0" level
    Then I validate the output of "policy-map_WAN_IN_MEA" section
    When I query the content of section "policy-map PARENT_WAN_OUT" at "0" level
    Then I validate the output of "policy-map_PARENT_WAN_OUT" section
    When I query the content of section "policy-map LAN_IN_TEST_VPN2" at "0" level
    Then I validate the output of "policy-map_LAN_IN_TEST_VPN2" section
    When I query the content of section "policy-map LAN_IN_Global" at "0" level
    Then I validate the output of "policy-map_LAN_IN_Global" section
    When I query the content of section "policy-map LAN_IN" at "0" level
    Then I validate the output of "policy-map_LAN_IN" section
    When I query the content of section "interface GigabitEthernet0/0/0" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/0" section
    When I query the content of section "interface GigabitEthernet0/0/1" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/1" section
    And I close the SSH connection

  @deleteService @TC_69 @TC_70
  Scenario Outline: Delete the created service for TC_69_and_TC_70 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "<testCaseNumber>" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

  Examples:
      |testCaseNumber|
      |69            |
      |70            |



