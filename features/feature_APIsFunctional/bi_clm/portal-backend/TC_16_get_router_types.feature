@tc13
Feature: Get architecture types
  This features validates api response for fetching all architecture types

  Scenario: Get all architecture types
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "fetch" request for "portal-backend"