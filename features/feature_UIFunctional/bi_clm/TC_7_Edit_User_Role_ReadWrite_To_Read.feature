@portal @tc7 @editUserRole
Feature: BI CLM Edit user role - Read/Write to Read 
  This feature tests the Edit user role functionality from read/write to read

  Scenario: Update from admin to read/write
    Given I read test data for testcase
    When I filter the "User" by "userName" and user "exist" in the results
    Then I validate that the portal user role "admin" is "unchecked"
    And I validate that the portal user role "write" is "checked"
    And I validate that the portal user role "read" is "checked"
    When I click on the "write" checkbox
    Then I validate the "userupdated" "success" alert "message"
    Then I wait for the "currentPage" to load
    When I filter the "User" by "userName" and user "exist" in the results
    Then I validate that the portal user role "admin" is "uchecked"
    And I validate that the portal user role "write" is "uchecked"
    And I validate that the portal user role "read" is "checked"
    Then I clear the "searchBox" field