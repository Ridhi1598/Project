@controller @tc2 @createService
Feature: Validate controller response for create service request
  This features validates controller response for timed out create service request

  Scenario: Create Service request timeout
    Given I set data values against testcase
    And I set l3vpn "RMQ" url
    And I set api endpoint for "publish" message for "sending"
    And I set request body for "publish" message for "sending"
    And Send request to "publish" message in RMQ queue
    And Validate that response body has "routed" as "true"
    And I set api endpoint for "read" message for "sending"
    And I set request body for "read" message for "sending"
    And Send request to "read" message in RMQ queue
    And Validate that there is no message in the RMQ queue
    And I set l3vpn "ES" url
    And I set api endpoint for "request" record for "read" ES message
    And I set request query for "request" record for "read" ES message
    And I validate that a "request" record is "created" in "l3vpn-controller-requests" index
    And I validate the "request_type" value in "external-request-tracker"
    And Validate a request id is returned by mediation layer as synchronous response
    And Wait for the callback response from "mediation layer"
    And I validate that a "request" record is "created" in "l3vpn-controller-requests" index
    And Validate that no callback response is returned by mediation layer