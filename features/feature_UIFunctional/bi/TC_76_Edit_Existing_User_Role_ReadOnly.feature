Feature: Edit existing user's role
  This feature tests the functionality of editing an existing user's role

  Scenario: Edit user role: From Read/Write to Read only
    Given I set data values against testcase "76"
    Given I should land on BI Home page
    Given "Home" page title should be "BI service dashboard"
    Then I navigate view by clicking on "UserManagement"
    Then "UserManagement" page title should be "User Management"
    Then User name should "be" displayed in the list of users
    And I validate that the user role "Read" is "enabled"
    And I validate that the user role "ReadWrite" is "enabled"
    And I validate that the user role "Admin" is "disabled"
    Then I change the user role to "Read" from "ReadWrite"
    Then User name should "be" displayed in the list of users
    And I validate that the user role "Read" is "enabled"
    And I validate that the user role "ReadWrite" is "disabled"
    And I validate that the user role "Admin" is "disabled"