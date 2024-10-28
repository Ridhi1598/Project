Feature: Cancel the service update request
  This feature tests the functionality of Cancelling a service update request which is in pending state

  Scenario: Update request from NC
    Given I set data values against testcase "17"
    When I read service id for UI testcase
    And I set BI "controller" url
    And I generate access token for authorization
    And I Set headers "Content" and "Authorization"
    And I Set api endpoint and request Body
    And I Set query parameters for controller request for "before"
    When I Send HTTP request for controller
    And I extract response value for expected "requestId"

  @updateConfigCancel
  Scenario: Cancel pending request origin: NC
    Given I set data values against testcase "68"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    And Validate that service request has "Operation" as "modify"
#    And I read the "old" "requestId" for "modify" scenario
    And Click on "reviewButton" button in service queue table to open "reviewModal"
    And Assert that "cancelButton" button is not displayed
