@TC_88
Feature: RollBack - Current version
  This feature tests the rollback button should be disabled for the current version

  Scenario: Rollback button should be disabled for the current version
    Given I read test data for BI_CLM UI testcase
    When "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    When I click on "advanceFilter" button
    Then I search the service by "CSID" only
    Then I go to "Services" page
    When I click on "rollback" button
    Then I wait for the loader to be disabled
    When I wait for the "parameterInformation" element to be visible
    Then I validate that the rollback button should be "disable"

