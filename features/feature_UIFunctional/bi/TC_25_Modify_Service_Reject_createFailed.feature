@portal @tc25
Feature: Modify Service Reject Scenario

  Scenario: Update a Non Existent Service : Operation create service - Failed
    Given I set data values against testcase "25"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "create service"
    And Validate that "operationResult" should be "FAILED"
    When Open "Parameter Information" box by expanding the row
    And Update "port" value for the service
    And I click on "Save" button
    And An "Alert" box should open
    And I validate the "error" message in the "Alert" box for "update"
    Then I click on "OK" button
    And I refresh the page and wait for the dashboard to load
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "modify service"
    And Validate that "operationResult" should be "REJECTED"
    And Validate same "error" message is displayed upon mouse hover on operation result link
    And Validate same "error" message is displayed upon clicking on alert button