@ISR_4221_2
Feature: TC_8: Create and Delete GRF and VRF specific BFD ipv4 and ipv6 config
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_6
  Scenario: Create/Update service with valid payload and in valid state with
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "6" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

  @createL3VPNService @TC_7
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "7" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    And I validate the IE response as "completed"

  @createL3VPNService @TC_8
  Scenario: Create and Delete GRF and VRF specific BFD ipv4 and ipv6 config
    Given I set L3VPN "REST" url
    When I set api endpoint for testcase "8" for l3vpn
    Then Set request Body for L3VPN
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    When I query the content of section "router bgp 65011" at "0" level
    Then I validate the output of "router-bgp-configurations" section
    And I validate the output of "address-family-ipv4" section
    And I validate the output of "address-family-ipv6" section
    And I validate the output of "address-family-ipv4-vrf" section
    And I validate the output of "address-family-ipv6-vrf" section
    When I query the content of section "interface GigabitEthernet0/0/0.2460" at "0" level
    Then I validate the output of "interface-GigabitEthernet-2460" section
    When I query the content of section "interface GigabitEthernet0/0/0.2461" at "0" level
    Then I validate the output of "interface-GigabitEthernet-2461" section
    And I close the SSH connection

  @deleteService @TC_66 @TC_67
  Scenario Outline: Delete the created service for TC_66_and_TC_77 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "<testCaseNumber>" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

  Examples:
      |testCaseNumber|
      |66            |
      |67            |

