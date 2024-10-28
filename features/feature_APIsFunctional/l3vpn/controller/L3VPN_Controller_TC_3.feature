@controller @tc3 @createService
Feature: Validate controller response for create service request
  This features validates controller response for successful create service request

  Scenario: Create Service request with success response from mediation
    Given I set data values against testcase
    When I set l3vpn "RMQ" url
    Then I set api endpoint for "publish" message for "sending"
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
#    And I validate record format for "request" response
    And Validate a callback response is returned by mediation layer as asynchronous response
    And Validate the "request_id" value in the response
    And Validate the "completed" value in the response
    And Validate the "state" value in the response
    And I set api endpoint for "service" record for "read" ES message
    And I set request query for "service" record for "read" ES message
    And I validate that a "service" record is "created" in "l3vpn-controller-services" index
#    And I validate record format for "service" response
#    Add service record validations
    And I set l3vpn "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    And Send request to "read" message in RMQ queue
    And Validate that a "success" message is published to controller
    And Validate response format for "success" message

  Scenario: Delete ES record for created service in "l3vpn-controller-services" index
    Given I set data values against testcase
    Given I set l3vpn "ES" url
    And I find document id for the created "services" record
    And I set api endpoint for "delete" a "services" record
    And I set api request body for "delete" a "services" record
    When I send HTTP request for "delete" service
    Then I validate that the "services" record is "deleted" in "l3vpn-controller-services" index

