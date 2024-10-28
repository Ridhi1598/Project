@controller
Feature: Validate controller response for display rollback request if concurrent requests count exceeds Rate Limit
  This features validates controller response for display rollback request if concurrent requests count exceeds Rate Limit

  Scenario: Update ES record for a create request record in "bi-controller-requests" index
    Given I set BI "ES" url
    And I set data values against test case "102"
    And I create a document id for request record creation
    And I set api endpoint for "create" a requests record
    And I set api request body for "create" a requests record
    When I send HTTP request for "create" service
    Then I validate that the requests record is "created"

  Scenario: Display rollback request against Rate Limit
    Given I set BI "controller" url
    And I set data values against test case "85"
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I validate the response schema
    And I validate response body for expected "status" and "reason"