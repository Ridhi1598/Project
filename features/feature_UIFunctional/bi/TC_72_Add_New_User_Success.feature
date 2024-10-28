Feature: Add New User in User Management
    This feature tests the functionality of adding a new user

  Scenario: Add user: Success
    Given I set data values against testcase "72"
    Given I should land on BI Home page
    Given "Home" page title should be "BI service dashboard"
    Then I navigate view by clicking on "UserManagement"
    Then "UserManagement" page title should be "User Management"
    And I navigate view by clicking on "AddNewUser"
    Then I fill user details and save
    Then Validate the alert message for "success"
    Then User name should "be" displayed in the list of users