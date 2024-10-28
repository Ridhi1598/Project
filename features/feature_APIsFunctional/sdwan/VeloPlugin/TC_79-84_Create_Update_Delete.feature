Feature:
  This feature tests the api calls related to the VPN

  Background:
    Given I generate access token for the authorization for Velo TCs
    When I set SDWAN "Velo" url

  Scenario: Creates a VPN
    When I set Test Data for testcase "79" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set POST api endpoint "/tinaa-sdwan-services=12/vpns?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "POST" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc79.json" for sdwan functional

  Scenario: Try to create an already existing segment
    When I set Test Data for testcase "80" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set POST api endpoint "/tinaa-sdwan-services=12/vpns?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "POST" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc80.json" for sdwan functional

  Scenario: Update a VPN for an enterprise
    When I set Test Data for testcase "81" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services=12/vpns=Segment2?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc81.json" for sdwan functional

  Scenario: Try to update a VPN that does not exist
    When I set Test Data for testcase "82" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/tinaa-sdwan-services=12/vpns=non-existent-vpn?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc82.json" for sdwan functional

  Scenario: Delete the VPN for a given enterprise
    When I set Test Data for testcase "83" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set DELETE api endpoint "/tinaa-sdwan-services=12/vpns=testing segment?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40&enterprise-id=2724" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "DELETE" of SDWAN Functional TCs

  Scenario: Try to delete a VPN that is being used in a vlan
    When I set Test Data for testcase "84" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set DELETE api endpoint "/tinaa-sdwan-services=12/vpns=office-net2?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40&enterprise-id=2724" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "DELETE" of SDWAN Functional TCs
