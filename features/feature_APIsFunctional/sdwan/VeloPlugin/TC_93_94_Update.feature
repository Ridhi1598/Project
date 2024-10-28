Feature:
  This feature tests the api calls related to the LAN

  Background:
    Given I generate access token for the authorization for Velo TCs
    When I set SDWAN "Velo" url

  Scenario: Update a Wan of a device that belongs to an enterprise
    When I set Test Data for testcase "93" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=Edge2/wan-access=GE4?enterprise-id=2646&callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc93.json" for sdwan functional

  Scenario: Try to update a non-existent wan interface
    When I set Test Data for testcase "94" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services=12/sites=11/devices/device=Edge2/wan-access=GE14?enterprise-id=2646&callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc94.json" for sdwan functional