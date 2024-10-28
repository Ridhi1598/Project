@tc2
Feature: Get specific customer details
  This features validates api response for fetching details of a specific customers

  Scenario: Get specific customer details
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "fetch" request for "portal-backend"
    Then I read "id" for the customer
    And I validate response for expected "customer_id"
    Then I Validate that a "customer" record is "found" in "ES" database
    And I validate the customer "id" is "mapped" in database
