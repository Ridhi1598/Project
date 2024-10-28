Feature: Change Account State
  This feature tests the functionality of changing an existing user's account state

  Scenario: Change Account State
    Given I should land on BI Home page
    Given "Home" page title should be "BI service dashboard"
    Then I navigate view by clicking on "UserManagement"
    When "UserManagement" page title should be "User Management"
    Then I search the User by the Username
    Then I click on "AccountState" button
    Then I click on "AlertYes" button
    Then I click on "AlertOK" button
    Then I search the User by the Username
    Then I click on "Read-Write" button
    Then I click on "AlertYes" button
    Then I click on "AlertOK" button
    Then I search the User by the Username
    Then I revoke the user "Read-Write" button
    Then I click on "AlertYes" button
    Then I click on "AlertOK" button
    Then I search the User by the Username
    Then I validate the user should be enabled