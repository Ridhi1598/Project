@portal @tc87 @portalFilter
Feature: Validate filter results based on single filter
  This feature validates filter results based on single filter

  Scenario: Validate filter results based on single filter: CSID
    Given I set data values against testcase "87"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "1" row should appear in results
    And Validate that search results should show "1" results