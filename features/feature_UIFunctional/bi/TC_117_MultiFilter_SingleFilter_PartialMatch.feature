@portal @tc117 @portalFilter
Feature: Validate filter results based on single filter
  This feature validates filter results based on single filter

  Scenario Outline: Validate filter results based on single filter: "<searchFilter>"
    Given I set data values against testcase "117"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "<searchFilter>" parameter
    And Wait for the search results to appear
    And Validate that all results have the expected result for "<searchFilter>" for "<matchType>" search

  Examples:
      |searchFilter         |matchType    |
      |serviceId            |partial      |
      |CustomerName         |partial      |
      |OperationType        |partial      |
      |OperationResult      |partial      |
      |NetworkElementName   |partial      |
      |NetworkType          |partial      |