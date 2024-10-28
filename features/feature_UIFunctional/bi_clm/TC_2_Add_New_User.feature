@portal @tc2
Feature: BI CLM User Management - Add new valid user
  This feature tests the login and logout functionality for BI Portal

  Scenario: User Management - Add new User
    Given I read test data for testcase
    When "UserManagement" page title should be "User Management"
    When I click on "addNewUser" button
    Then Wait for the "createUserPopup" popup to appear
    When I validate that all the fields should be clear
    Then I enter "userName" details for "read" role
    When I click on "create" button
    Then I validate the alert Message for "success" Service
#    Then I validate the "usercreated" "success" alert "message"
    And I wait for the "currentPage" to load
    And I filter the "User" by "userName" and user "exist" in the results
    Then I clear the "searchBox" field
 