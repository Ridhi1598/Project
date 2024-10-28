@portal @tc5 @editUserRole
Feature: BI CLM Edit User Role - Read/Write to admin
  This feature tests the Edit User Role from Read/Write to admin

  Scenario: Update from read/write to admin
    Given I read test data for testcase
    When I filter the "User" by "userName" and user "exist" in the results
    Then I validate that the portal user role "admin" is "unchecked"
    And I validate that the portal user role "write" is "checked"
    And I validate that the portal user role "read" is "checked"
    When I click on the "admin" checkbox
    Then I validate the "userupdated" "success" alert "message"
    Then I wait for the "currentPage" to load
    When I filter the "User" by "userName" and user "exist" in the results
    Then I validate that the portal user role "admin" is "checked"
    And I validate that the portal user role "write" is "checked"
    And I validate that the portal user role "read" is "checked"
    Then I clear the "searchBox" field

