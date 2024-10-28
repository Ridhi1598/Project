@ASR920-6
Feature: TC:16 Create and Delete base vrf test
  This feature tests the api calls related to the creating and deleting L3VPN services

  Background: Generating access-token
    Given I generate access token for L3VPN

  @CreateL3VPNService @TC_16
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "16" for l3vpn
    And I set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I Create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    Then I query the content of section "vrf definition TEST_VPN_BASE_ASR_6" at "0" level
    Then I validate the output of "vrf_definition_TEST_VPN_BASE_ASR_6" section
    And I close the SSH connection

  @deleteService @TC_76
  Scenario: Delete and created service for "TC_76" which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "76" for l3vpn
    Then I set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"