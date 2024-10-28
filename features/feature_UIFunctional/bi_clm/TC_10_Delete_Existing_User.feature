@portal @tc10 @userManagement
Feature: BI CLM User Management-Delete Existing User
  This feature tests the login and logout functionality for BI Portal

  Scenario: User Management-Delete Existing User
    Given I read test data for testcase
    When I should land on "Home" page
    Then "Home" page title should be "Services"
    When I click on "UserManagement" button
    Then "UserManagement" page title should be "User Management"
    When I clear the "searchBox" field
    Then I filter the "User" by "userName" and user "exist" in the results
    When I click on "deleteUser" icon
    Then Wait for the "deleteConfirmation" popup to appear
    When I click on "confirm" button
    Then I validate the "userdeleted" "success" alert "message"
    And I filter the "User" by "userName" and user "does'nt exist" in the results
#    And I click on "servicesSidebar" button

