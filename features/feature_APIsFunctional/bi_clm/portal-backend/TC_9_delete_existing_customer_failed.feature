@tc9
Feature: Delete existing customer
  This features validates api response for fetching all customers

  Scenario: Add new customer: Failed
    Given I read test data for testcase
    When I send request to "create-service" record in "ES" "service" record
    And I generate access token for authorization
    When I Send "delete-customer" request for "portal-backend"
    And I validate response for expected "status"
    And I validate response for expected "reason"
    And I Validate that a "customer" record is "found" in "ES" database
    When I send request to "delete-service" record in "ES" "service" record