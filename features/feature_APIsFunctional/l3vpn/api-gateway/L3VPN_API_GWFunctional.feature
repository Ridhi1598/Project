@l3vpn @apiGateway
Feature: Validate API-Gateway Response for L3VPN
  This feature tests the functional test cases related to the API Gateway

Background:
  Given I set L3VPN "REST" url

@health
  Scenario: Validate if the API Gateway is up
    When I set data values against scenario "Health API" for API Gateway
    When I Set "GET" api endpoint for "/health" for L3VPN
    When Send "GET" HTTP request for API Gateway
    Then I receive valid HTTP response code "200" for "GET"
    And I validate the response value of API Gateway for "Health API"

@noAuthToken
  Scenario: Validate response against no authentication token
    When I set data values against scenario "No token authentication" for API Gateway
    Then I Set "POST" api endpoint for "/l3vpn/svc/v1/service" for L3VPN
    When I Set HEADER param request "Content-Type" as "application/json"
    And Set request Body for api gateway APIs of L3VPN
    And Send "POST" HTTP request for API Gateway
    Then I receive valid HTTP response code "401" for "POST"
    And I validate the response schema with "No_token_authentication.json"
    And I validate the response value for expected message of API Gateway

@expiredAuthToken
  Scenario: Validate response against expired authentication token
    When I set data values against scenario "Expired token authentication" for API Gateway
    When I Set "POST" api endpoint for "/l3vpn/svc/v1/service" for L3VPN
    When I Set HEADER param request "Content-Type" as "application/json"
    Then I Set HEADER param request "Authorization" for "Expired token authentication" for API Gateway
    And Set request Body for api gateway APIs of L3VPN
    And Send "POST" HTTP request for API Gateway
    Then I receive valid HTTP response code "401" for "POST"
    And I validate the response schema with "Expired_token_authentication.json"
    And I validate the response value for expected message of API Gateway

  @incorrectAuthToken
  Scenario: Validate response against expired authentication token
    When I set data values against scenario "Wrong token authentication" for API Gateway
    When I Set "POST" api endpoint for "/l3vpn/svc/v1/service" for L3VPN
    When I Set HEADER param request "Content-Type" as "application/json"
    Then I Set HEADER param request "Authorization" for "Wrong token authentication" for API Gateway
    And Set request Body for api gateway APIs of L3VPN
    And Send "POST" HTTP request for API Gateway
    Then I receive valid HTTP response code "401" for "POST"
    And I validate the response schema with "Wrong_token_authentication.json"
    And I validate the response value for expected message of API Gateway

@keycloakCert
  Scenario: Validate if keycloak certificate exists
    When I set data values against scenario "Keycloack certificate validation" for API Gateway
    When I Set "POST" api endpoint for "/l3vpn/svc/v1/service" for L3VPN
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Authorization" for "Wrong token authentication" for API Gateway
    And Set request Body for api gateway APIs of L3VPN
    And Send "POST" HTTP request for API Gateway
    Then I receive valid HTTP response code "400" for "POST"
    And I validate the response schema with "Keycloack_certificate_validation_1.json"
    And I validate the response value for expected message of API Gateway

@routePost
  Scenario: Validate route check for create service
    When I set data values against scenario "Routing service validation-1" for API Gateway
    When I Set "POST" api endpoint for "/l3vpn/svc/v1/service" for L3VPN
    When I Set HEADER param request "Content-Type" as "application/json"
    And I Set HEADER param request "Authorization" for "Routing service validation-1" for API Gateway
    And Set request Body for api gateway APIs of L3VPN
    And Send "POST" HTTP request for API Gateway
    Then I receive valid HTTP response code "400" for "POST"
    And I validate the response schema with "Routing_service_validation-1.json"
    And I validate the response value for expected message of API Gateway