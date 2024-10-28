Feature: Duplicate User Registration
  This feature tests the functionality of Duplicate user validation

  @duplicateUser
  Scenario: Validate a duplicate user cannot be added
    Given I set data values against testcase "85"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I navigate view by clicking on "UserManagement"
    Then "UserManagement" page title should be "User Management"
    Then  User name should "be" displayed in the list of users
    Then I navigate view by clicking on "AddNewUser"
    Then Fill the pre-existed user details
    Then Validate the alert message for "error"