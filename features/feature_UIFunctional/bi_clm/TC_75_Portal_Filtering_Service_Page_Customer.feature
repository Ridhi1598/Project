@portal @tc75
Feature: Portal filtering- Services page
  This feature tests the Portal filtering by Customer field from Service page

  Scenario: This scenario test the search functionality based on the Customer field by validating multiple results
    Given I read test data for testcase
    When I click on "advanceFilter" button
    Then I search the Service by using "Customer" value from advance filter
    When I validate that the searched result should appear for "Customer" value in Service details table
    Then I click on "clearAllFilter" button