@portal @tc62
Feature: Portal filtering- WorkOrders page
  This feature search the result based on non-existing values- Operation type, Status, Network type

  Scenario: This scenario test the search functionality based on non-existing values- Operation type, Status, Network type
    Given I read test data for testcase
    Then I click on "WorkOrders" button
    When I go to "WorkOrders" page
#    When I fetch the information of first record from "WorkOrders Details page"
    Then I click on "advanceFilter" button
    When I search WorkOrders details by using "non_existing_values" value from advance filter
    Then I validate that the searched result should appear for "non_existing_values" value in WorkOrders details table
    Then I click on "clearFilterTransaction" button


