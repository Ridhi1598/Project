@ingestion @portalCall
Feature: Validate ingestion response for portal call
  This features validates ingestion response for default portal call

@portalCall
  Scenario: Default portal call with result in descending order
    Given I read test data for testcase
    And I generate access token for authorization
    And I Send "portal" request for "ingestion"
    And Validate that response is sorted in "descending" order according to "request-timestamp"