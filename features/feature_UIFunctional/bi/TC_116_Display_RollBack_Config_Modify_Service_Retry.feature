Feature: Display RollBack Current and Expected Config
  This feature tests the functionality of initiating a display rollback config call from BI Portal

  Scenario: Display Rollback Current and Expected Config : Retry with success response
    Given I set data values against testcase "116"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    And Validate that service request has "Operation" as "rollback"
    And I search for the "old" "RequestID" for "rollback" scenario from dashboard
    And Click on "reviewButton" button in service queue table to open "reviewModal"
    And  Assert that "Retry" is displayed
    When I click on "Retry" button
    And I click on "Close" button
    Then Click on "reviewButton" button in service queue table to open "reviewModal"
    And Assert that response for "current" config is "In Progress ..."
    And Assert that response for "expected" config is "In Progress ..."
    Then Mock "display-current-config-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    Then Mock "display-expected-config-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And Assert that response for "current" config is "expectedValue"
    And Assert that response for "expected" config is "expectedValue"
    And Assert that "Retry" button is not displayed