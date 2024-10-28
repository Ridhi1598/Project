@controller @portalCall @multiFilter
Feature: Validate controller response for portal call for search with single filter and invalid search term
  This features validates controller response for portal for search with single filter and invalid search term

@portalCall
  Scenario: Portal call with no search results
    Given I set BI "controller" url
    And I set data values against test case "131"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And Validate that "no" records for the search are returned