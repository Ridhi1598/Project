Feature: Retry button for delete on Work Orders page

  Scenario: This scenario tests the clickability of Retry button- delete
    Given I read test data for testcase
#    Then I click on "WorkOrders" button
#    Then I go to "WorkOrders" page
    And I click on "clearFilter" button
    Then I click on "advanceFilter" button
    And I search WorkOrders details by using "Operation_Type_and_Status" value from advance filter
    Then I find the "Retry" is present