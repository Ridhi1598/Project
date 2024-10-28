Feature:
  This feature tests the api calls related to the Customer

  Background:
    Given I generate access token for the authorization for Velo TCs
    When I set SDWAN "Velo" url

  Scenario: Creates a SDWAN enterprise customer
    When I set Test Data for testcase "76" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set POST api endpoint "/bsaf-telus-ext-customer?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "POST" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc76.json" for sdwan functional

  Scenario: Updates SDWAN enterprise customer given by enterprise-id in the request body
    When I set Test Data for testcase "77" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/bsaf-telus-ext-customer=8?callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "PUT" of SDWAN Functional TCs
    And I validate the response schema with "velo_tc77.json" for sdwan functional

  Scenario: Try to delete an enterprise with existing edges
    When I set Test Data for testcase "78" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set DELETE api endpoint "/bsaf-telus-ext-customer=8?enterprise-id=1036&callback-url=https://jsonplaceholder.typicode.com/posts&timeout=40" for the Velo testcases
    And Send HTTP request for SDWAN Functional TCs
    And I receive valid HTTP response code 200 for "DELETE" of SDWAN Functional TCs





