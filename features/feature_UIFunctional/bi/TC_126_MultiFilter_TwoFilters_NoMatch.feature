@portal @tc124 @portalFilter
Feature: Validate filter results based on single filter
  This feature validates filter results based on single filter

  Scenario: Validate filter results based on all filters and partial match
    Given I set data values against testcase "126"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    Then I filter and search the "OperationType" parameter
    And Wait for the search results to appear
    And Validate that no search result is displayed
    And Validate that search results should show "0" results