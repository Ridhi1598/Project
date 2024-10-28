@portal @tc23
Feature: Modify Service Reject Scenario

  Scenario: Update a Non Existent Service : Operation delete service - Completed
    Given I set data values against testcase "23"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    When Validate that "operationType" should be "delete service"
    And Validate that "operationResult" should be "COMPLETED"
    Then Expand the row and validate the error message is "Data Not Available!"