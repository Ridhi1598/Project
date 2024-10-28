@portal @tc12 @userManagement
Feature: BI CLM User Management-Add user details input validation
  This feature tests the login and logout functionality for BI Portal

  Scenario: User Management-Add user details input validation
    Given I read test data for testcase
    When I click on "UserManagement" button
    Then "UserManagement" page title should be "User Management"
    Then I wait for the "currentPage" to load
    And I click on "addNewUser" button
    And I click on "create" button
    But I validate the "userName" field "error" message
    And I validate the "userRole" field "error" message
    And I click on "cancel" button