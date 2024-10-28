@apiGateway
Feature: Validate API-Gateway Response
  This feature tests the functional test cases related to the API Gateway

@health
  Scenario: Validate if the API Gateway is up
    Given I set BI "REST" url
    When I set data values against scenario "Health API"
    When I Set "GET" api endpoint for "/health" for BI
#    And Send "GET" HTTP request
    Then I receive valid HTTP response code "200" for "GET"
    And I validate the response value for "Health API"