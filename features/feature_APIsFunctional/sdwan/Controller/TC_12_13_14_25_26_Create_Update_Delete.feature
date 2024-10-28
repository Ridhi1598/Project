Feature: SDWAN Customer APIs
  This feature tests the api calls related to Create PUT and Delete SDWAN Customer APIs

  Background:
    Given I generate access token for the authorization of SDWAN Functional Tcs
    When I set SDWAN "Functional" url

  @TC12 @TC25 @ReadListAllCustomer
  Scenario: Lists all SDWAN customers
    When I set Test Data for testcase "25" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I set GET api endpoint "/bsaf-telus-ext-customer" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  @TC12 @CreateCustomer
  Scenario: creates a SDWAN Customer
    When I set Test Data for testcase "12" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    Then I Set POST posts api endpoint for "/bsaf-telus-ext-customer" API of sdwan Functional
    And Set request Body for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    Then I extract cust-id from the response after creating a customer


  @TC12 @TC26 @ReadCustomer
   Scenario: returns the given SDWAN customer
    When I set Test Data for testcase "26" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set GET api endpoint "/bsaf-telus-ext-customer/{cust-id}" for SDWAN Functional TCs
    And Send HTTP request for SDWAN Functional TCs
    When I receive valid HTTP response code 200 for "GET" of SDWAN Functional TCs

  @TC12 @TC13 @UpdateCustomer
  Scenario: updates the given SDWAN customer
    When I set Test Data for testcase "13" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    And I set PUT api endpoint "/bsaf-telus-ext-customer/{cust-id}" for SDWAN Functional TCs
    And Set request Body for SDWAN Functional TCs
    Then Set the Updated values of payload for update a Customer
    And Send HTTP request for SDWAN Functional TCs
    Then I extract requestId from response of "PUT" request for ElasticSearch Database Validation
    Then I perform ElasticSearch Database Validation for "PUT" request

  @TC12 @TC14 @DeleteCustomer
  Scenario: Delete Customer
    When I set Test Data for testcase "14" of SDWAN Functional TCs
    When I Set HEADER param request "Content-Type" as "application/json" for SDWAN Functional TCs
    Then I Set HEADER param request "Authorization" as "access-token" for SDWAN Functional TCs
    When I set Delete api endpoint "/bsaf-telus-ext-customer/{cust-id}" for SDWAN Functional Tcs
    And Send HTTP request for SDWAN Functional TCs
    Then I extract requestId from response of "DELETE" request for ElasticSearch Database Validation
    Then I perform ElasticSearch Database Validation for "DELETE" request