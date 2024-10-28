@portal @tc142
Feature: Resource Validation for change port value rollback scenario

  Scenario: Rollback Change Port : Display Config : Success
    Given I set data values against testcase "142"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "modify service"
    And Validate that "operationResult" should be "COMPLETED"
    And I search for the "old" "RequestID" for "rollback" scenario from dashboard
    When I click on "HistoryButton" and "History" Modal should open
    Then I validate the "old" "RequestID" for "rollback" scenario in history modal
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
    And Validate that "old" and "new" "RequestID" are "different" for "rollback"
    And Assert that "Edit" button is not displayed
    And Assert that response for "current" config is "In Progress ..."
    And Assert that response for "expected" config is "In Progress ..."
    And I click on "Close" button
    And Validate the service is available in service queue
    And Validate that service request has "Operation" as "rollback"
    And Validate that service request has "Origin" as "TINAA"
    Then Click on "reviewButton" button in service queue table to open "reviewModal"
    And I set BI "controller" url
    And I Set api endpoint and request Body
    Then Mock "display-current-config-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    Then Mock "display-expected-config-success" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And Assert that response for "current" config is "expectedValue"
    And Assert that response for "expected" config is "expectedValue"
    And Assert that "Retry" button is not displayed