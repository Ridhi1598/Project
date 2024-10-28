Feature: SDWAN Services APIs
  This feature tests the api calls related to Create Patch SDWAN service

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs
    When I set SDWAN "Functional" url

  @TC1 @TC15 @ReadService
  Scenario: Read Services
    When I set Test Data for testcase "15" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract response value of service-id and cust-id for SDWAN Functional TCs

  @TC1 @CreateService
  Scenario: Create Service
    When I set Test Data for testcase "1" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I Set POST posts api endpoint for "/tinaa-sdwan-services" API of sdwan Functional
    And Set request Body for SDWAN Functional TCs
    And Set the updated values of payload for create services POST API
    And Send HTTP request for SDWAN Functional TCs

  @TC1 @TC16 @ReadServiceById
  Scenario: Read Services by Id
    When I set Test Data for testcase "16" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services/{service-id}" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs


  @TC1 @TC2 @UpdateServiceById
  Scenario: Patch Service
    Given I set Test Data for testcase "2" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I set Patch api endpoint "/tinaa-sdwan-services/{service-id}" for SDWAN Functional TCs
    And Set request Body for SDWAN Functional TCs
    And I Set the updated fields of payload for Patch Service
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "PATCH" of SDWAN Functional TCs
    Then I extract requestId from response of "PATCH" request for ElasticSearch Database Validation
    Then I perform ElasticSearch Database Validation for "PATCH" request



