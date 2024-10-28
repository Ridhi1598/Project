@portal @tc76
Feature: Portal filtering- Service
  This feature tests the Portal filtering by Non-existing CSID from Service page

  Scenario: This scenario test the search functionality by Non-existing CSID
    Given I read test data for testcase
#    When I navigate to "services" page
    Then "Home" page title should be "Services"
    Then I click on "advanceFilter" button
    When I search the Service by using "non_existing_CSID" value from advance filter
    Then I validate that the searched result should appear for "non_existing_CSID" value in Service details table
    Then I click on "clearAllFilter" button


