@tc8
Feature: Delete existing customer
  This features validates api response for fetching all customers

  Scenario: Delete existing customer: Success
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "delete-customer" request for "customer-catalog"
    Then I validate the expected response schema
    And I validate response for expected "status"
    And I validate response for expected "result"
    And I Validate that a "customer" record is "not found" in "ES" database