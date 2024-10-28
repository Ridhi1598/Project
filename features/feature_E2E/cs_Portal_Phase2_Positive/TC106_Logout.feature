@portal @tc106
Feature: Logout
  This feature tests the Log out functionality

  Scenario: tc_105: User Management - Add new User
    Given I set data values against testcase "106"
    When I click on "profileDropdown" button
    Then I click on "signOut" button
    When I go to "Landing"
    Then Wait for the "Login" popup to appear
