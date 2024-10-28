@portal @tc1
Feature: BI Portal Login
  This feature tests the login and logout functionality for BI Portal

  Background: Read Test Data
    Given I read test data for testcase

  Scenario: Log in to BI Portal-Admin Access
    Given I should land on "Home" page
    When "Home" page title should be "Services"
    Then I wait for the "currentPage" to load
    And I validate that "UserManagement" is "visible"