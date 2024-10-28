@portal @tc74
Feature: Portal filtering- Services page
  This feature tests the Portal filtering by CSID, Customer, Customer Name

  Scenario: This scenario test the search functionality based on CSID, Customer, Customer Name
    Given I read test data for testcase
    When I click on "advanceFilter" button
    Then I search the Service by using "CSID_Customer_Name" value from advance filter
    When I validate that the searched result should appear for "CSID_Customer_Name" value in Service details table
    Then I click on "clearAllFilter" button
