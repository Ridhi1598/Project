@ASR920-6
Feature: TC:17 Create and Delete Global BGP config
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_17
  Scenario:Create/Update service with valid payload and valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "17" for L3VPN
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    Then I query the content of section "router bgp 65026" at "0" level
    Then I validate the output of "router_bgp_65026" section
    And I close the SSH connection

  @deleteService @TC_77
  Scenario:Delete the create service for TC_77 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "77" for L3VPN
    Then I set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
