@apiGateway @tc1
Feature: Validate API-Gateway Response
  This feature tests the functional test cases related to the API Gateway

@healthCheck
  Scenario: Validate the route
    Given I read test data for testcase
    And I set "api-gateway" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "api-gateway" api endpoint
    And I Set "api-gateway" api request body
    And I Set query parameters for "api-gateway" request for "before"
    When I Send HTTP request for "api-gateway"
    And I validate the expected response schema
    Then I validate response should have "status" as expected response
    And I validate response should have "reason" as expected response
    And I validate response should have "code" as expected response