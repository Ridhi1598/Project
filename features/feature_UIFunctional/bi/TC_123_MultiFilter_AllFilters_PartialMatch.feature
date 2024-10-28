@portal @tc123 @portalFilter
Feature: Validate filter results based on single filter
  This feature validates filter results based on single filter

  Scenario: Validate filter results based on all filters and partial match
    Given I set data values against testcase "123"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    Then I filter and search the "CustomerName" parameter
    Then I filter and search the "OperationType" parameter
    Then I filter and search the "OperationResult" parameter
    Then I filter and search the "NetworkElementName" parameter
    Then I filter and search the "NetworkType" parameter
    And Wait for the search results to appear
    And Validate that all results have the expected result for "serviceId" for "partial" search
    And Validate that all results have the expected result for "CustomerName" for "partial" search
    And Validate that all results have the expected result for "OperationType" for "partial" search
    And Validate that all results have the expected result for "OperationResult" for "partial" search
    And Validate that all results have the expected result for "NetworkElementName" for "partial" search
    And Validate that all results have the expected result for "NetworkType" for "partial" search