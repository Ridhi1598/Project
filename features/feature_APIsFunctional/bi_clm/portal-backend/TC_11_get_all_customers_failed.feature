@tc11
Feature: Get all customers
  This features validates api response for fetching all customers

  Scenario: Get all customers Failed
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "fetch" request for "portal-backend"
    And I validate response for expected "status"
    And I validate response for expected "reason"