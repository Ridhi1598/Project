@tc7
Feature: Edit existing customer
  This features validates api response for fetching all customers

  Scenario: Edit existing customer: Failed
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "update-customer" request for "customer-catalog"
    Then I validate the expected response schema
    And I validate response for expected "status"
    And I validate response for expected "reason"
    And I Validate that a "customer" record is "found" in "ES" database