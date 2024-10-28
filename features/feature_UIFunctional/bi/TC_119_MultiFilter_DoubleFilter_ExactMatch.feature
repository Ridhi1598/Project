@portal @tc117 @portalFilter
Feature: Validate filter results based on single filter
  This feature validates filter results based on single filter

  Scenario: Validate filter results based on single filter: "<searchFilter>"
    Given I set data values against testcase "119"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    Then I filter and search the "CustomerName" parameter
    And Wait for the search results to appear
    And Validate that all results have the expected result for "serviceId" for "exact" search
    And Validate that all results have the expected result for "CustomerName" for "exact" search