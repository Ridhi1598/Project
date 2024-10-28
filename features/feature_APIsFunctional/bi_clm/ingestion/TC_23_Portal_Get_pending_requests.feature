@ingestion @portalCall
Feature: Validate ingestion response for portal call for pending requests
  This features validates ingestion response for portal call for pending requests

@portalCall
  Scenario: Portal call for pending requests
    Given I read test data for testcase
    And I generate access token for authorization
    And I Send "portal" request for "ingestion"
    And Validate that all records are sorted in "descending" order according to "Request Timestamp"
    Then Validate all records have request "State" as "pending"