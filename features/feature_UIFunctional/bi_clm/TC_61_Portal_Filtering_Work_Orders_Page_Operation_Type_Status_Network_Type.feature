@portal @tc61
Feature: Portal filtering- WorkOrders page
  This feature search results based on multiple values- Operation type, Status, Network type

  Scenario: This scenario test the search functionality based on multiple values- Operation type, Status, Network type
    Given I read test data for testcase
#    Then I click on "clearFilterTransaction" button
    When I click on "advanceFilter" button
    Then I search WorkOrders details by using "OperationType_Status_NetworkType" value from advance filter
    When I validate that the searched result should appear for "OperationType_Status_NetworkType" value in WorkOrders details table
    And I click on "servicesSidebar" button

