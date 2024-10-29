@ASR920-6
Feature: TC_19: Create and Delete GRF standard sub-interface, default ports
  This feature tests the api calls related to creating and deleting a L3VPN Service

  Background: Generating access-token
    Given I generate access token for L3VPN

  @CreateL3VPNService @TC_19
  Scenario: Create/Update service with valid payload and in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "19" for L3VPN
    And I set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I set HEADER param request "Authorization" as "access-token" for L3VPN
    When Set request Body for L3VPN
    Then Send Http request for L3VPN
    Then I validate the IE response as "completed"
    When I create SSH connection to the device "user"
    Then I run "show running-config" command and store the device config
    Then I query the content of section "interface GigabitEthernet0/0/4" at "0" level
    Then I validate the output of "interface_GigabitEthernet0/0/4" section
    Then I validate the value of "encapsulation dot1q" section
    And I close the SSH connection

  @deleteService @TC_79
  Scenario: Delete and created service for "TC_79" which is in valid state
    When I set L3VPN "REST" url
    Then I set api endpoint for testcase "79" for L3VPN
    Then I set HEADER param request "Content-Type" as "application/json" for L3VPN
    And I Set HEADER param request "Authorization" as "access-token" for L3VPN
    And Set request Body for L3VPN
    When Send Http request for L3VPN
    Then I validate the IE response as "completed"

