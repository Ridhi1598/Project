Feature:
  This feature tests the api calls related to the Devices

  Background:
    Given I generate access token for the authorization for Velo TCs
    When I set SDWAN "Velo" url

  Scenario: Creates a site for a given enterprise and assigns to it a configuration profile
    When I set Test Data for testcase "85" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set POST api endpoint "/tinaa-sdwan-services=12/sites?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "POST" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc85.json" for sdwan functional

  Scenario: Try to create a device with a name that already exists
    When I set Test Data for testcase "86" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set POST api endpoint "/tinaa-sdwan-services=12/sites?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "POST" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc86.json" for sdwan functional

  Scenario: Updates a given device for a given enterprise
    When I set Test Data for testcase "87" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services=12/sites=14?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc87.json" for sdwan functional

  Scenario: Try to update a non-existent device
    When I set Test Data for testcase "88" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services=12/sites=14?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc88.json" for sdwan functional

  Scenario: Delete a device for a given enterprise
    When I set Test Data for testcase "89" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set DELETE api endpoint "/tinaa-sdwan-services=12/sites=14?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40&enterprise-id=2646&device-id=edgee2" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "DELETE" of SDWAN Functional TCs

  Scenario: Try to delete a non-existent device
    When I set Test Data for testcase "90" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set DELETE api endpoint "/tinaa-sdwan-services=12/sites=14?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40&enterprise-id=2646&device-id=non-existent-device" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "DELETE" of SDWAN Functional TCs
