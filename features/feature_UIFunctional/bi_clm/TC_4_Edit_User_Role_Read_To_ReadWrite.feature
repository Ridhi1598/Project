@portal @tc4 @editUserRole
Feature: BI CLM Edit User Role - Read to ReadWrite
  This feature tests the Edit User Role functionality from read only to read/write 

  Scenario: Update from read only to read/write
    Given I read test data for testcase 
    When I filter the "User" by "userName" and user "exist" in the results
    Then I validate that the portal user role "admin" is "unchecked"
    And I validate that the portal user role "write" is "unchecked"
    And I validate that the portal user role "read" is "checked"
    When I click on the "write" checkbox
    Then I validate the "userupdated" "success" alert "message"
    Then I wait for the "currentPage" to load
    When I filter the "User" by "userName" and user "exist" in the results
    Then I validate that the portal user role "admin" is "unchecked"
    And I validate that the portal user role "write" is "checked"
    When I validate that the portal user role "read" is "checked"
    Then I clear the "searchBox" field
