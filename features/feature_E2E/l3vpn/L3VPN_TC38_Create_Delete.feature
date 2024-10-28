@OA2501-1
Feature: TC_38: Create and Delete VRF sub-interface standard sub-interface, default ports
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @createL3VPNService @TC_38
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "38" for l3vpn
    Then I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"
    And I create SSH connection to the device "user"
    When I run "show running-config interface gigabitethernet 0/1.345" command and store the device config
    Then I validate the output of "interface_gigabitethernet_0/1.345" section at "default-level"
    And I close the SSH connection

  @deleteService @TC_98
  Scenario: Delete the created service for TC_98 which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "98" for l3vpn
    And I Set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

