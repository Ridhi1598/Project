Feature: Delete an Existing User
  This feature tests the functionality of deleting an existing user

  Scenario: Delete user: Success
    Given I set data values against testcase "79"
    And I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "UserManagement"
    And "UserManagement" page title should be "User Management"
    And User name should "be" displayed in the list of users
    When I delete the user
    And Validate the alert message for "success"
    And I verify that the user has been deleted
    And User name should "not be" displayed in the list of users
    Then I log out
    And "Landing" page title should be "TINAA BUSINESS INTERNET SERVICES"