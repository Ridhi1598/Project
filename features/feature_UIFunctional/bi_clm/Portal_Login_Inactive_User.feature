@portal @tc34
Feature: BI Portal Login
  This feature tests the login and logout functionality for BI Portal


  Scenario: Log in to BI Portal-Read/Write access
    Given I read test data for testcase
    And I should land on "Home" page
    When "Home" page title should be "Services"
    Then I wait for the "current page" to load
    And I validate that "UserManagement" is "not visible"