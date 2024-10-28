@portal @tc60
Feature: Portal filtering- Work Orders page
  This feature tests the search functionality by CSID field from W Page

  Scenario: This Scenario tests the search functionality by CSID field
    Given I read test data for testcase
    Then I go to "WorkOrders" page
    When I wait for the "WorkOrders" to load
    When I fetch the information of first record from "WorkOrders Details page"
    Then I click on "advanceFilter" button
    When I search WorkOrders details by using "CSID" value from advance filter
    Then I validate that the searched result should appear for "CSID" value in WorkOrders details table

