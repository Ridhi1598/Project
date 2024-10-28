@portal @tc73
Feature: Portal filtering- Services page
  This feature tests the Portal filtering by CSID field

  Scenario: this scenario test the search functionality based on CSID
    Given I read test data for testcase
    When I fetch the information of first record from "Service Details page"
    Then I click on "advanceFilter" button
    When I search the Service by using "CSID" value from advance filter
    Then I validate that the searched result should appear for "CSID" value in Service details table
    Then I click on "clearAllFilter" button