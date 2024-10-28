@portal @tc88 @portalFilter
Feature: Validate filter results based on single filter
  This feature validates filter results based on single filter

  Scenario Outline: Validate filter results based on single filter: "<searchFilter>"
    Given I set data values against testcase "88"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "<searchFilter>" parameter
    And Wait for the "<searchFilter>" search results to appear as expected
    And Validate that all results have the expected result for "<searchFilter>" for "<matchType>" search

    Examples:
      |searchFilter         |matchType  |
      |serviceId            |exact      |
      |CustomerName         |exact      |
      |OperationType        |exact      |
      |OperationResult      |exact      |
      |NetworkElementName   |exact      |
      |NetworkType          |exact      |