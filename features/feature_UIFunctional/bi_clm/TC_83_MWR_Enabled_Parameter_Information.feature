@portal @tc83
Feature: MWR - Enabled on Parameter Information
  This feature tests the MWR should be enabled on Parameter information

  Scenario: This scenario validates that the MWR should be enabled on Parameter information
    Given I read test data for BI_CLM UI testcase
    Then "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    When I click on "advanceFilter" button
    Then I search the service by "CSID" only
    Then I go to "Services" page
    When I click on "rollback" button
    Then I wait for the loader to be disabled
    And I wait for the "parameterInformation" element to be visible
    Then I validate that the MWR details should be "enabled"
    And I click on "servicesSidebar" button