Feature: Retry button for Update on Work Orders page

  Scenario: This scenario tests the clickability of Retry button- Update
    Given I read test data for testcase
    Then I click on "WorkOrders" button
    Then I go to "WorkOrders" page
    Then I click on "advanceFilter" button
    Then I search WorkOrders details by using "Operation_Type_and_Status" value from advance filter
    Then I find the "Retry" is present