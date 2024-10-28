@controller @portalCall
Feature: Validate controller response for portal call
  This features validates controller response for portal call with parameters

@portalCall
  Scenario: Portal call with results for TM Case
    Given I set BI "controller" url
    And I set data values against test case "46"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And Validate the response has correct values against each key
    And Validate that "CIU Name" in response is not a null value