@portal @tc100
Feature: User Management - Add new user
  This feature tests the add new user functionality

  Scenario: tc_100 :User Management - Add new User
    Given I set data values against testcase "100"
    When I should land on CS Home page
    Then "Home" page title should be "Dashboard"
    When I click on "UserManagement" button
    When "UserManagement" page title should be "User Management"
    When I click on "addNewUser" button
    Then Wait for the "addNewUserTitle" popup to appear
    Then Fill the required information to add a new user with "read-only" access rights
    When I click on "Add1" button
    Then I filter the user by "user" and the searched user "should" be present in the results
#    Then I confirm that the read-only box should remain checked
#    When I click on "profileDropdown" button
#    When I click on "signOut" button
#    Then I go to "Landing"
#    Then Wait for the "Login" popup to appear
#    Then I login into the application with read-only user
#    When I go to "Home"
#    Then I validate that the "UserManagement" option should not be visible for read-only user
#    When I expand the "L2Topology" sidebar
#    Then I navigate view by clicking on "OLT"