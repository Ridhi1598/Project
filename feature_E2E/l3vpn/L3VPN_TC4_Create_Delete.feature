@ISR_4221_2
Feature: TC_4: Create and Delete Global BGP config
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_4
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "4" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    And I create SSH connection to the device "user"
    And I run "show running-config" command and store the device config
    When I query the content of section "router bgp 65011" at "0" level
    Then I validate the output of "router-bgp-configurations" section
    And I validate the output of "address-family-ipv4" section
    And I validate the output of "address-family-ipv6" section
    When I query the content of section "interface GigabitEthernet0/0/1.452" at "0" level
    Then I validate the output of "interface-configurations" section
    And I close the SSH connection

  @deleteService @TC_64
  Scenario: Delete the created service for TC_64 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "64" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

