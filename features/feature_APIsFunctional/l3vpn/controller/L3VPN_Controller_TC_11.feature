@controller @tc11 @deleteService
Feature: Validate controller response for delete service request
  This features validates controller response for successful delete service request

  Scenario: Update ES record for a create service in "l3vpn-controller-services" index
    Given I set data values against testcase
    Given I set l3vpn "ES" url
    Given I create and assign document id for record creation
    And I set api endpoint for "create" a "services" record
    And I set api request body for "create" a "services" record
    When I send HTTP request for "create" service
    Then I validate that the "services" record is "created" in "l3vpn-controller-services" index
    And I set api endpoint for "service" record for "read" ES message
    And I set request body for "service" record for "read" ES message
    And I validate that a "service" record is "created" in "l3vpn-controller-services" index

  Scenario: delete service request failure due to error from mediation
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
    And I validate record format for "request" response
    And Validate a callback response is returned by mediation layer as asynchronous response
    And Validate the "request_id" value in the response
    And Validate the "completed" value in the response
    And Validate the "state" value in the response
    And I set api endpoint for "service" record for "read" ES message
    And I set request query for "request" record for "read" ES message
    And I validate that a "service" record is "not created" in "l3vpn-controller-services" index
    And I set l3vpn "RMQ" url
    And I set api endpoint for "read" message for "callback"
    And I set request body for "read" message for "callback"
    And Send request to "read" message in RMQ queue
    And Validate that a "success" message is published to controller
    And Validate response format for "success" message