@controller @portalCall
Feature: Validate controller response for portal call
  This features validates controller response for default portal call

@portalCall
  Scenario: Default portal call with result in descending order
    Given I set BI "controller" url
    And I set data values against test case "34"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And Validate the response is sorted in "descending" order according to "request-timestamp"
#    And Validate that no duplicate records are returned for service-id