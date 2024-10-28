@portal @tc81
Feature: MWR Service Details
  This feature tests the MWR Service Details functionality

  Scenario: This scenario test the functionality related to MWR Service Details
    Given I read test data for BI_CLM UI testcase
    When I validate that the "advanceFilter" button should be clickable
    Then I click on "advanceFilter" button
    When I search the service by "CSID" only
    Then I click on "firstEdit" button
    When I click on "serviceEditDetails" button
    Then I validate that the MWR details should be "enabled"
    And I click on "servicesSidebar" button