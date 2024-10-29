@tc102 @userManagement
Feature: User Management-Search for user - by email
  This feature tests the functionality relarted to search the user - by email

  Scenario: User Management-Delete Existing User
    Given I set data values against testcase "102"
    When I should land on CS Home page
    Then "Home" page title should be "Dashboard"
    When I click on "UserManagement" button
    Then "UserManagement" page title should be "User Management"
    When I clear the "searchBox" field
    Then I filter the user by "email" and the searched user "should" be present in the results
