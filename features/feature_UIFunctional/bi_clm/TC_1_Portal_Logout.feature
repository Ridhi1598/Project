@portal @tc1
Feature: BI Portal Login
  This feature tests the login and logout functionality for BI Portal

  Scenario: Log out from BI Portal
    Given I read test data for testcase
    When I click on "userProfile" button
    Then I click on "logout" button
    And "Landing" page title should be "Business Systems Automation Framework ( BSAF)"
