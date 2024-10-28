@portal @tc124 @portalFilter
Feature: Validate filter results based on single filter
  This feature validates filter results based on single filter

  Scenario: Validate filter results based on all filters and partial match
    Given I set data values against testcase "129"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    Then I filter and search the "CustomerName" parameter
    Then I filter and search the "OperationType" parameter
    Then I filter and search the "OperationResult" parameter
    Then I filter and search the "NetworkElementName" parameter
    Then I filter and search the "NetworkType" parameter
    And Wait for the search results to appear
    When Clear the search field "serviceId"
    When Clear the search field "CustomerName"
    When Clear the search field "OperationType"
    When Clear the search field "OperationResult"
    When Clear the search field "NetworkElementName"
    When Clear the search field "NetworkType"
    And Wait for the search results to appear
#    And Validate that default dashboard is displayed