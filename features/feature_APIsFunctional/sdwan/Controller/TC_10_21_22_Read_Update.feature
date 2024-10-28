Feature: SDWAN LAN Access APIs
  This feature tests the api calls related to Read and Update LAN Access APIs

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs
    When I set SDWAN "Functional" url

  @TC10 @TC15 @ReadServices
  Scenario: Read Services
    When I set Test Data for testcase "15" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract response value of service-id and cust-id for SDWAN Functional TCs

  @TC10 @TC19 @ReadAllSitesList
  Scenario: Lists all SDWAN sites in given SDWAN service
    When I set Test Data for testcase "19" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I set GET api endpoint "/tinaa-sdwan-services/{service-id}/sites" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract site-id from list of all Sites for SDWAN Functional TCs
    Then I extract device-id for the corresponding site-id

  @TC10 @TC21 @ReadListAllLAN
  Scenario: Returns a list of LAN interfaces in a given device in a given site in given SDWAN service
    When I set Test Data for testcase "21" of SDWAN Functional TCs
    Then I set GET api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/lan-access" for SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract name from the list of LAN Interface

  @TC10 @UpdateLANInterface
  Scenario: Updates the given LAN interface in a given device in a given site in given SDWAN service
    When I set Test Data for testcase "10" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/lan-access/{name}" for SDWAN Functional TCs
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    Then I extract requestId from response of "PUT" request for ElasticSearch Database Validation
    Then I perform ElasticSearch Database Validation for "PUT" request

  @TC10 @TC22 @ReadALLLAN
  Scenario: Returns the given LAN interface in a given device in a given site in given SDWAN service
    When I set Test Data for testcase "22" of SDWAN Functional TCs
    Then I set GET api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/lan-access/{name}" for SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

