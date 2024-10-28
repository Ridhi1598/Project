@tc3
Feature: Get non existing customer
  This features validates api response for fetching all customers

  Scenario: Get all customers
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "fetch" request for "portal-backend"
    And I validate response for expected "total-size"
    And I Validate that a "customer" record is "not found" in "ES" database