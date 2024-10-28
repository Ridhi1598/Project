@tc18
Feature: Get all requests details
  This features validates api response for fetching all requests details

  Scenario: Get all architecture types
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "fetch" request for "portal-backend"