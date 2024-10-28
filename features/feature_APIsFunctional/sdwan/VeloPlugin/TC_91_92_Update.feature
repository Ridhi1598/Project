Feature:
  This feature tests the api calls related to the LAN

  Background:
    Given I generate access token for the authorization for Velo TCs
    When I set SDWAN "Velo" url

  Scenario: Updates a given device for a given enterprise
    When I set Test Data for testcase "91" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=Edge2/lan-access=GE2?enterprise-id=2646&callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc91.json" for sdwan functional

  Scenario: Updates a given device for a given enterprise
    When I set Test Data for testcase "92" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=Edge2/wan-access=GE4?enterprise-id=2646&callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc92.json" for sdwan functional
