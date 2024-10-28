@portal @tc102
Feature: Validate only supported port speeds are displayed
  This feature validates only supported port speeds are displayed

  @createService
  Scenario: Validate only supported port speeds are displayed
    Given I set data values against testcase "102"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    Given Filter and search the "serviceId" for update request
    When Open "Parameter Information" box by expanding the row
    And I click on "portSpeed" button
    Then Validate that only supported port speeds are displayed