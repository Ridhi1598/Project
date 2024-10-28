@tc10
Feature: Get all customers
  This features validates api response for fetching all customers

  Scenario: Get all customers : Failed
    Given I read test data for testcase
    When I Send "fetch" request for "customer-catalog"
    And I validate response for expected "status"
    And I validate response for expected "reason"