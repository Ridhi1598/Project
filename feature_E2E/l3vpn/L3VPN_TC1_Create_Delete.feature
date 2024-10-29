@ISR_4221_2
Feature: TC_1: Create and Delete Base VPN service
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_1
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "1" for l3vpn
    Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    And I create SSH connection to the device "user"
    When I run "show running-config" command and store the device config
    Then I query the content of section "vrf definition TEST_VPN_BASE_IPv4_1" at "0" level
    Then I validate the output of "vrf-configurations" section
    And I close the SSH connection

  @deleteService @TC_61
  Scenario: Delete the created service for TC_61 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "61" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

