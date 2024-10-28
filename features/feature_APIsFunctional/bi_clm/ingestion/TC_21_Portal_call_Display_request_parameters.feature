@ingestion @portalCall
Feature: Validate ingestion response for portal call
  This features validates ingestion response for portal call with parameters

@portalCall
  Scenario: Portal call with results
    Given I read test data for testcase
    And I generate access token for authorization
    And I Send "portal" request for "ingestion"
    And Validate the "CIU Name" in response is not a null value
