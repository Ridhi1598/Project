@portal @tc30
Feature: Update Service with Success display config response

  Scenario: Update Service : Display Config : Success
    Given I set data values against testcase "30"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And I search for the "old" "RequestID" for "update" scenario from dashboard
    When Open "Parameter Information" box by expanding the row
    And Update "port" value for the service
    And I click on "Save" button
    And An "Alert" box should open
    And I validate the "success" message in the "Alert" box for "update"
    Then I click on "OK" button
    And "ServiceQueue" page title should be "Service Update Queue"
    And Assert that "reviewModal" is displayed
    And Validate that a "new" "RequestID" is generated for "update"
    And Validate that "old" and "new" "RequestID" are "different" for "update"
    And Assert that "Edit" is displayed
    And Assert that response for "current" config is "In Progress ..."
    And Assert that response for "expected" config is "In Progress ..."
    And I click on "Close" button
    And Validate the service is available in service queue
    And Validate that service request has "Operation" as "modify"
    And Validate that service request has "Origin" as "TINAA"
    Then Click on "reviewButton" button in service queue table to open "reviewModal"
    And I set BI "controller" url
    And I Set api endpoint and request Body
    Then Mock "display-current-config-failed" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    Then Mock "display-expected-config-failed" response to be published to RMQ "tinaa-bi-request-callbacks" queue
    And Assert that response for "current" config is "expectedValue"
    And Assert that response for "expected" config is "expectedValue"
    And Assert that "Retry" is displayed