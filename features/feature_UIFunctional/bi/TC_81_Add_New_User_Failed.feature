Feature: Add New User in User Management
    This feature tests the functionality of adding a new user

  Scenario: Add user: Failed
    Given I set data values against testcase "81"
    Given I should land on BI Home page
    Given "Home" page title should be "BI service dashboard"
    Then I navigate view by clicking on "UserManagement"
    Then "UserManagement" page title should be "User Management"
    And I navigate view by clicking on "AddNewUser"
    Then I leave all the details empty and try to save
    And I navigate view by clicking on "AddNewUser"
    Then I fill details except user role and try to save
    And I navigate view by clicking on "AddNewUser"
    Then I fill details except TelusID and try to save
