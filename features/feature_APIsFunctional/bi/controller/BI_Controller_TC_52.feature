@controller @portalCall
Feature: Validate controller response for portal call for pending requests
  This features validates controller response for portal call for pending requests

@portalCall
  Scenario: Portal call for pending requests
    Given I set BI "controller" url
    And I set data values against test case "52"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And Validate all records are sorted in "descending" order according to "Request Timestamp"
    Then Validate that all records have request "State" as "pending"
    And Validate that no duplicate records are returned for "Service ID"