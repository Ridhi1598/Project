@tc5
Feature: Add new customer
  This features validates api response for fetching all customers

  Scenario: Add new customer: Failed
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "create-customer" request for "portal-backend"
    And I validate response for expected "status"
    And I validate response for expected "result"
    And I Validate that a "customer" record is "found" in "ES" database