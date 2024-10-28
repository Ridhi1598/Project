@controller @portalCall
Feature: Validate controller response for portal call for historical data
  This features validates controller response for portal call with result in descending order

@portalCall
  Scenario: Portal call with result in ascending order and search by text
    Given I set BI "controller" url
    And I set data values against test case "36"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And Validate the response is sorted in "descending" order according to "site-id"
    Then Validate that only records with service-id "site-id" are returned