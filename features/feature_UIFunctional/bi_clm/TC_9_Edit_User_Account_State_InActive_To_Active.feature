@portal @tc9 @editUserAccount
Feature: BI CLM Edit User Account state - Inactive to Active
  This feature tests the Edit User Account functionality from Inactive to Active

  Scenario: Change user account state from Inactive to Active
    Given I read test data for testcase
    When I clear the "searchBox" field
    Then I filter the "User" by "userName" and user "exist" in the results
    When I validate that the portal user account "state" is "disabled"
    Then I wait for the "state" to load and click on it
    Then I wait for the loader to be disabled
#    When I validate the alert Message for "success" Service
    When I validate the "userupdated" "success" alert "message"
    Then I wait for the "currentPage" to load
    When I filter the "User" by "userName" and user "exist" in the results
    Then I validate that the portal user account "state" is "enabled"
    Then I clear the "searchBox" field
    And I click on "servicesSidebar" button