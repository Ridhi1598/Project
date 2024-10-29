@tc103 @userManagement
Feature: User Management- Change user role
  This feature tests the functionality related to change the user role

  Scenario: User Management- Change user's role
    Given I set data values against testcase "103"
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I click on "UserManagement" button
    Then "UserManagement" page title should be "User Management"
    When I clear the "searchBox" field
    Then I filter the user by "email" and the searched user "should" be present in the results
    Then I change the user role from "read-only" to "read-write"
    Then Wait for the loader to disappear
    Then I clear the "searchBar" from User management screen
    Then I filter the user by "email" and the searched user "should" be present in the results
    Then I validate that the "read-write" role should be selected for the user
    Then I validate that the read-only user should be selected
    Then I clear the "searchBar" from User management screen