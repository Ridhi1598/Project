@portal @tc45
Feature: Update parameters for Execute Request - Success
  This feature tests the functionality related to update parameters for Execute Request - Success

  Scenario: Tests the functionality related to update parameters for Execute Request - Success
    Given I read test data for testcase
    When I should land on "Home" page
    Then "Home" page title should be "Services"
    And I validate that the "ServiceUpdate" button should be clickable
    And I click on "ServiceUpdate" button
    When "ServiceUpdate" page title should be "Service Update Queue"
    When I click on "firstRequestServiceUpdateQueue" button
    And I wait for the loader to be disabled
    And I validate that the "Execute" button should not be visible for read-only user
