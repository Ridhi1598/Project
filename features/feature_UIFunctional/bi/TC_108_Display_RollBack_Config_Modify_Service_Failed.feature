Feature: Display RollBack Current and Expected Config
  This feature tests the functionality of initiating a display rollback config call from BI Portal

  Scenario: Display Rollback Current and Expected Config : Failed to fetch Current config
    Given I set data values against testcase "108"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "modify service"
    And Validate that "operationResult" should be "COMPLETED"
    And I search for the "old" "RequestID" for "rollback" scenario from dashboard
    When I click on "HistoryButton" and "History" Modal should open
    Then I validate the "old" Request ID for "rollback" scenario
    And "RollBack" should be available in "Actions" column for latest transaction
    Then I click on "RollBack" button
    And An "Confirmation" box should open
    And I validate the "confirm" message in the "Confirmation" box for "rollback"
    And I click on "Continue" button
    And An "Alert" box should open
    And I validate the "success" message in the "Alert" box for "rollback"
    And I click on "OK" button
    And "ServiceQueue" page title should be "Service Update Queue"
    And Assert that "reviewModal" is displayed
    And Validate that a "new" "RequestID" is generated for "rollback"
    And I set BI "controller" url
    And I Set api endpoint and request Body
    And Validate that "old" and "new" "RequestID" are "different" for "rollback"
    And Assert that "Edit" button is not displayed
    And Assert that response for "current" config is "In Progress ..."
    And Assert that response for "expected" config is "In Progress ..."
    And I click on "Close" button
    And Validate the service is available in service queue
    And Validate that service request has "Operation" as "rollback"
    And Validate that service request has "Origin" as "TINAA"
    Then Click on "reviewButton" button in service queue table to open "reviewModal"
    Then Mock "display-current-config-failed" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    Then Mock "display-expected-config-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And Assert that response for "current" config is "expectedValue"
    And Assert that response for "expected" config is "expectedValue"
    And Assert that "Retry" is displayed