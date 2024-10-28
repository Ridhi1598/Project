@portal @tc133
Feature: Validate filter results based on single filter
  This feature validates filter results based on single filter

  Scenario: Validate filter results based on all filters and partial match
    Given I set data values against testcase "133"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    When I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Open "Parameter Information" box by expanding the row
    Then Validate that the "IPV4CustomerPrefix0" field is "disabled"
