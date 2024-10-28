@controller @portalCall @multiFilter
Feature: Validate controller response for portal call for search with single filter and exact match
  This features validates controller response for portal for search with single filter and exact match

@portalCall
  Scenario: Portal call with result in descending order and search by exact CSID
    Given I set BI "controller" url
    And I set data values against test case "120"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And Validate that "expected" records for the search are returned
    And I validate the response schema
    And Validate the response is sorted in "descending" order for "exact" match of "site-id"
    Then Validate that only records with "exact" match for "site-id" are returned