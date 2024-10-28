@controller @portalCall @multiFilter
Feature: Validate controller response for portal call for search with all filters and partial match
  This features validates controller response for portal for search with all filters and partial match

@portalCall
  Scenario: Portal call with result in descending order and search by partial match
    Given I set BI "controller" url
    And I set data values against test case "134"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And Validate that "expected" records for the search are returned
    And I validate the response schema
    Then Validate that only records with "partial" match for "site-id" are returned
    Then Validate that only records with "partial" match for "request-type" are returned
    Then Validate that only records with "partial" match for "request-state" are returned
    Then Validate that only records with "partial" match for "customer-name" are returned
    Then Validate that only records with "partial" match for "pe-device-id" are returned
    Then Validate that only records with "partial" match for "network-type" are returned