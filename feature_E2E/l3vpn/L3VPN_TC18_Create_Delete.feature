@ASR920-6
Feature: TC_18: Create and Delete VRF BGP Config
  This feature tests the api calls related to creating and deleting L3VPN service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @CreateL3VPNService @TC_18
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "18" for L3VPN
    And I set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    When I query the content of section "router bgp 65026" at "0" level
    Then I validate the output of "router_bgp_65026" section
    And I close the SSH connection

  @deleteService @TC_78
  Scenario: Delete and Created service for TC_78 which is valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "78" for l3vpn
    Then I set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
