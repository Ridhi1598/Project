@ISR_4221_2
Feature: TC_6: Create and Delete GRF specific BFD ipv4 and ipv6 config
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_6
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "6" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    When I query the content of section "router bgp 65011" at "0" level
    Then I validate the output of "router-bgp-configurations" section
    Then I validate the output of "address-family-ipv4" section
    Then I validate the output of "address-family-ipv6" section
    When I query the content of section "interface GigabitEthernet0/0/0.2460" at "0" level
    Then I validate the output of "interface-configurations" section
    And I close the SSH connection

  @deleteService @TC_66
  Scenario: Delete the created service for TC_66 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "66" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

