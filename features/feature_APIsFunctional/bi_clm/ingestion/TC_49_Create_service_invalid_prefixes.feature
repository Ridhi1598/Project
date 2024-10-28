@ingestion @createService
Feature: Validate controller response for create service request
  This features validates controller response for create service with invalid ipv4 prefixes

  Scenario: Create Service: Reject: Invalid ipv4 prefixes
    Given I read test data for testcase
    And I set "ingestion" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set "ingestion" api endpoint
    And I Set "ingestion" api request body
    And I Set query parameters for "ingestion" request for "before"
    When I Send HTTP request for "ingestion"
    And I validate the expected response schema
   And I validate the response body for expected "status" and "reason"
    And I validate response should have "code" as expected response