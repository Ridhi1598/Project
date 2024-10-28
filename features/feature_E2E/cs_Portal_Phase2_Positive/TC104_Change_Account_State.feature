@tc104 @userManagement
Feature: User Management- Change account state from active to in-active
  This feature tests the functionality related to change the account state from active to in-active

  Scenario: User Management- Change account state
    Given I set data values against testcase "104"
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I click on "UserManagement" button
    Then "UserManagement" page title should be "User Management"
    When I clear the "searchBox" field
    Then I filter the user by "email" and the searched user "should" be present in the results
    Then I change the account state from "active" to "inactive"
    Then Wait for the loader to disappear
    Then I filter the user by "email" and the searched user "should" be present in the results
    Then I validate that the selected user should be in "inactive" state
    Then I clear the "searchBar" from User management screen