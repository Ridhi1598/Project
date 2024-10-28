Feature: SDWAN Device License
  This feature tests the api calls related to Create PUT and Delete SDWAN Customer APIs

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs
    When I set SDWAN "Functional" url

  @TC29 @ReadDeviceLicense
  Scenario: returns SDWAN device licenses information
    When I set Test Data for testcase "29" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I set GET api endpoint "/bsaf-sdwan-device-licenses" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

