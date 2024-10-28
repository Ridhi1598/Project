Feature: SDWAN Config Templates
  This feature tests the api calls related to Read SDWAN Config Templates

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs
    When I set SDWAN "Functional" url

  @TC28 @ReadTemplates
  Scenario: returns SDWAN configuration templates for different resources such as VPNs and devices
    When I set Test Data for testcase "28" of SDWAN Functional TCs
    Then I set GET api endpoint "/bsaf-sdwan-templates" for SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

