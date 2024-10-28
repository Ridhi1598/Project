@apiGateway
Feature: Validate API-Gateway Response
  This feature tests the functional test cases related to the API Gateway

Background:
  Given I set BI "REST" url

@health
  Scenario: Validate if the API Gateway is up
    When I set data values against scenario "Health API"
    When I Set "GET" api endpoint for "/health" for BI
    And Send "GET" HTTP request
    Then I receive valid HTTP response code "200" for "GET"
    And I validate the response value for "Health API"

@noAuthToken
  Scenario: Validate response against no authentication token
    When I set data values against scenario "No token authentication"
    When I Set "POST" api endpoint for "/bi/mpls/v1/service"
    When I Set HEADER param request "Content-Type" as "application/json"
    And Set request Body for "/bi/mpls/v1/service" API of BI
    And Send "POST" HTTP request
    Then I receive valid HTTP response code "401" for "POST"
    And I validate the response schema with "No_token_authentication.json"
    And I validate the response value for expected message

@expiredAuthToken
  Scenario: Validate response against expired authentication token
    When I set data values against scenario "Expired token authentication"
    When I Set "POST" api endpoint for "/bi/mpls/v1/service"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Authorization" for "Expired token authentication"
    And Set request Body for "/bi/mpls/v1/service" API of BI
    And Send "POST" HTTP request
    Then I receive valid HTTP response code "401" for "POST"
    And I validate the response schema with "Expired_token_authentication.json"
    And I validate the response value for expected message

@incorrectAuthToken
  Scenario: Validate response against incorrect authentication token
    When I set data values against scenario "Wrong token authentication"
    When I Set "POST" api endpoint for "/bi/mpls/v1/service"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Authorization" for "Wrong token authentication"
    And Set request Body for "/bi/mpls/v1/service" API of BI
    And Send "POST" HTTP request
    Then I receive valid HTTP response code "401" for "POST"
    And I validate the response schema with "Wrong_token_authentication.json"
    And I validate the response value for expected message

@keycloakCert
  Scenario: Validate if keycloak certificate exists
    When I set data values against scenario "Keycloack certificate validation"
    When I Set "POST" api endpoint for "/bi/mpls/v1/service"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Authorization" for "Keycloack certificate validation"
    And Set request Body for "/bi/mpls/v1/service" API of BI
    And Send "POST" HTTP request
    Then I receive valid HTTP response code "400" for "POST"
    And I validate the response schema with "Keycloack_certificate_validation_1.json"
    And I validate the response value for expected message

@routePost
  Scenario: Validate route check for create service
    When I set data values against scenario "Routing service validation-1"
    Given I Set "POST" api endpoint for "/bi/mpls/v1/service"
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Authorization" for "Routing service validation-1"
    And Set request Body for "/bi/mpls/v1/service" API of BI
    And Send "POST" HTTP request
    Then I receive valid HTTP response code "400" for "POST"
    And I validate the response schema with "Routing_service_validation-1.json"
    And I validate the response value for expected message

@routeFetch
  Scenario: Validate route check for fetching service data
    When I set data values against scenario "Routing service validation-2"
    When I Set "GET" api endpoint for "/bi/mpls/v1/requests"
    When I Set query parameters for request
    And I Set HEADER param request "Authorization" for "Routing service validation-2"
    And Send "GET" HTTP request
    Then I receive valid response code "202" or "500" for "GET"
    And I validate the response schema with "Routing_service_validation-2.json"
