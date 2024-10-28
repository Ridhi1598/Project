Feature: SDWAN Services APIs
  This feature tests the api calls related to Create Patch and Delete SDWAN service

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs

  @TC1 @DeleteService
  Scenario: Delete Service
    When I set SDWAN "Functional" url
    When I set Test Data for testcase "3" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I set Delete api endpoint "/tinaa-sdwan-services/{service-id}" for SDWAN Functional Tcs
    And Send HTTP request for SDWAN Functional TCs