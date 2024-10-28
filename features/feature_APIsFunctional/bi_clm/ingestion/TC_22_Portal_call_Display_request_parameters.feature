@ingestion @portalCall @multiFilter
Feature: Validate controller response for portal call for search with single filter and exact match
  This features validates controller response for portal for search with single filter and exact match

@portalCall
  Scenario: Portal call with result in descending order and search by exact request-type
    Given I read test data for testcase
    And I generate access token for authorization
    And I Send "portal" request for "ingestion"

