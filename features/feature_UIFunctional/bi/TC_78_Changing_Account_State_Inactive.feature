Feature: Change User Account State
  This feature tests the functionality of changing an existing user's account state

  Scenario: Change Account State : Inactive to Active
    Given I set data values against testcase "78"
    Given I should land on BI Home page
    Given "Home" page title should be "BI service dashboard"
    Then I navigate view by clicking on "UserManagement"
    Then "UserManagement" page title should be "User Management"
    Then User name should "be" displayed in the list of users
    And I validate that the account state is "inactive"
    Then I change the account state to "active"
    Then User name should "be" displayed in the list of users
    Then I verify that the account state has been changed
    And I validate that the account state is "active"