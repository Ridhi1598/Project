@portal @tc3 @userManagement
Feature: BI CLM User Management-Add new invalid user
  This feature tests the login and logout functionality for BI Portal

  Scenario: User Management-Add invalid user
    Given I read test data for testcase
    When I wait for the "currentPage" to load
    Then "UserManagement" page title should be "User Management"
    And I click on "addNewUser" button
    And Wait for the "createUserPopup" popup to appear
    When I enter "userName" details for "read" role
    Then I click on "create" button
    And I validate the "usercreated" "error" alert "message"
    And I filter the "User" by "userName" and user "does'nt exist" in the results
    And I clear the "searchBox" field