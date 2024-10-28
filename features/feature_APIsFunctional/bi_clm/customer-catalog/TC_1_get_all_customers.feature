@tc1
Feature: Get all customers
  This features validates api response for fetching all customers

  Scenario: Get all customers Success
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "fetch" request for "customer-catalog"