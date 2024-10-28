Feature: SDWAN WAN Access APIs
  This feature tests the api calls related to Read and Update WAN Access APIs

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs
    When I set SDWAN "Functional" url

  @TC11 @TC15 @ReadServices
  Scenario: Generate Access token and Read Services
    When I set Test Data for testcase "15" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    When I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/tinaa-sdwan-services" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract response value of service-id and cust-id for SDWAN Functional TCs

  @TC11 @TC19 @ReturnListAllSites
  Scenario: Lists all SDWAN sites in given SDWAN service
    When I set Test Data for testcase "19" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I set GET api endpoint "/tinaa-sdwan-services/{service-id}/sites" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract site-id from list of all Sites for SDWAN Functional TCs
    Then I extract device-id for the corresponding site-id

  @TC11 @TC23 @ReturnListAllWan
  Scenario: Returns a list of WAN interfaces in a given device in a given site in given SDWAN service
    When I set Test Data for testcase "23" of SDWAN Functional TCs
    Then I set GET api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/wan-access" for SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs
    Then I extract name from the list of WAN Interface

  @TC11 @UpdateWanInterface
  Scenario: Updates the given WAN interface in a given device in a given site in given SDWAN service
    When I set Test Data for testcase "11" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/wan-access/{name}" for SDWAN Functional TCs
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    Then I extract requestId from response of "PUT" request for ElasticSearch Database Validation
    Then I perform ElasticSearch Database Validation for "PUT" request

  @TC11 @TC24 @ReadWanInterface
  Scenario: Returns the given WAN interface in a given device in a given site in given SDWAN service
    When I set Test Data for testcase "24" of SDWAN Functional TCs
    Then I set GET api endpoint "/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/wan-access/{name}" for SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs