@portal @tc105
Feature: User Management - Add new user with no values
  This feature tests the add new user with no values

  Scenario: tc_105: User Management - Add new User
    Given I set data values against testcase "105"
#    When I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#    When I click on "UserManagement" button
    When "UserManagement" page title should be "User Management"
    When I click on "addNewUser" button
    Then Wait for the "addNewUserTitle" popup to appear
    When I click on "Add1" button
#    When I validate the error message while adding the new user with empty values
    Then I validate the input field validation for "telus-id" is "User Id is required"
#    Then I validate the input field validation for "user-name" is "User Name is required"
#    Then I validate the input field validation for "email-id" is "Email Id is required"
#    And I click on "cancel" button

