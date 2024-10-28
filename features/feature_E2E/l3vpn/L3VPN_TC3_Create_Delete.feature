@ISR_4221_2
Feature: TC_3: Create and Delete VRF sub-interface
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createUpdateL3VPNService @TC_3
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    And I set api endpoint for testcase "3" for l3vpn
    When I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    And Send Http request for L3VPN
    And I validate the IE response as "completed"
    And I create SSH connection to the device "user"
    And I run "show running-config" command and store the device config
    And I query the content of section "vrf definition TEST_VPN_STANDARD_ENCAPSULATION" at "0" level
    Then I validate the output of "vrf-configurations" section
    And I query the content of section "interface GigabitEthernet0/0/1.345" at "0" level
    Then I validate the output of "interface-configurations" section
    And I close the SSH connection

  @deleteService @TC_63
  Scenario: Delete the created service for TC_63 which is in valid state
    When I set L3VPN "REST" url
    When I set api endpoint for testcase "63" for l3vpn
    When I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    And Send Http request for L3VPN
    And I validate the IE response as "completed"