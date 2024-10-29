@ASR920-6
Feature: TC_30: Create GRF rip routing
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_30
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "30" for L3VPN
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set Header param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    When I query the content of section "router rip" at "0" level
    Then I validate the output of "router_rip" section
    When I query the content of section "interface GigabitEthernet0/0/2" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/2" section
    Then I validate the value of "encapsulation dot1q" section
    And I close the SSH connection

  @deleteService
  Scenario:Delete the created service for TC_90 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "90" for L3VPN
    Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"