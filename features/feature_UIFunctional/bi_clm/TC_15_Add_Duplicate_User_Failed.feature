@portal @tc15 @userManagement
Feature: BI CLM User Management-Add duplicate user
  This feature tests the login and logout functionality for BI Portal

  Scenario: User Management-Add duplicate user
    Given I read test data for testcase
    When I should land on "Home" page
    When "Home" page title should be "Services"
    Then I wait for the "current page" to load
    And I navigate to "UserManagement" view
    When "UserManagement" page title should be "User Management"
    Then I wait for the "current page" to load
    And I click on "addNewUser" button
    And Wait for the "createUserPopup" popup to appear
    When I enter "userName" details for "read" role
    And I click on "create" button
    Then I validate the "userexisting" "error" alert "message"
    When I filter the user by "userName" and user "exist" in the results
