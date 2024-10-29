@tc101 @userManagement
Feature: User Management-Delete Existing User
  This feature tests the login and logout functionality for BI Portal

  Scenario: User Management-Delete Existing User
    Given I set data values against testcase "101"
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I click on "UserManagement" button
    Then "UserManagement" page title should be "User Management"
    Then I clear the "searchBar" from User management screen
    Then I filter the user by "user" and the searched user "should" be present in the results
    When I click on "deleteUser" button
    Then Wait for the "deleteConfirmation" popup to appear
    When I click on "deleteConfirm" button
    Then I validate the "success" message for deleting the user
    Then I filter the user by "user" and the searched user "should not" be present in the results

