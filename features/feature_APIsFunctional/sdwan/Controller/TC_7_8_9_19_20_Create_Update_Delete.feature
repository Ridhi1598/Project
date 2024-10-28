Feature: SDWAN Site APIs
  This feature tests the api calls related to Create PUT and Delete SDWAN Site

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs
    When I set SDWAN "Functional" url


  @TC7 @TC15 @ReadServices
  Scenario: Generate Access token and Read Services
    When I set Test Data for testcase "15" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract response value of service-id and cust-id for SDWAN Functional TCs

  @TC7 @TC19 @ReadALLSitesList
  Scenario: Lists all SDWAN sites in given SDWAN service
    When I set Test Data for testcase "19" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I set GET api endpoint "/tinaa-sdwan-services/{service-id}/sites" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract site-id from list of all Sites for SDWAN Functional TCs

  @TC7 @CreateSite
  Scenario: creates a SDWAN site in given SDWAN service
    When I set Test Data for testcase "7" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I Set POST posts api endpoint for "/tinaa-sdwan-services/{service-id}/sites" API of sdwan Functional
    And Set request Body for SDWAN Functional TCs
    And Set the Updated values of payload for creates a SDWAN site
    And Send HTTP request for SDWAN Functional TCs

   @TC7 @TC20 @ReadSitesList
   Scenario: Returns a list of sites in given SDWAN service
    When I set Test Data for testcase "20" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  @TC7 @TC8 @UpdateSite
  Scenario: updates a SDWAN VPN in given SDWAN service
    When I set Test Data for testcase "8" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}" for SDWAN Functional TCs
    And Set request Body for SDWAN Functional TCs
    Then Set the Updated values of payload for update a SDWAN site
    And Send HTTP request for SDWAN Functional TCs
    Then I extract requestId from response of "PUT" request for ElasticSearch Database Validation
    Then I perform ElasticSearch Database Validation for "PUT" request

  @TC7 @TC9 @DeleteSite
  Scenario: Delete Site
    When I set Test Data for testcase "9" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I set Delete api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}" for SDWAN Functional Tcs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "DELETE" of SDWAN Functional TCs
