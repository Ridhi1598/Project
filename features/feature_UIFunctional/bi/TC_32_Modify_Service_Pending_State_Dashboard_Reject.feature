Feature:Modify a service in pending state
  This feature tests the functionality of Modify service in pending state and validation

  Scenario: Modify a service in pending state
    Given I set data values against testcase "32"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    And I click on "Dashboard" button
    When "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    When Open "Parameter Information" box by expanding the row
    And Update "port" value for the service
    And I click on "Save" button
    And An "Alert" box should open
    And I validate the "error" message in the "Alert" box for "update"
    Then I click on "OK" button
    And I click on "HistoryButton" and "History" Modal should open
    And "userID" should be available in "User ID" column for latest transaction
