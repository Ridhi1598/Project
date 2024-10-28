@portal @tc8 @editUserAccount
Feature: BI CLM Edit User Account state - Active to Inactive
  This feature tests the Edit User Account functionality from Active to Inactive

  Scenario: Change user account state from Active to Inactive
    Given I read test data for testcase
    When I clear the "searchBox" field
    Then I filter the "User" by "userName" and user "exist" in the results
    When I validate that the portal user account "state" is "enabled"
    Then I wait for the "state" to load and click on it
    Then I wait for the loader to be disabled
    Then I validate the "userupdated" "success" alert "message"
    When I filter the "User" by "userName" and user "exist" in the results
    Then I validate that the portal user account "state" is "disabled"
    Then I clear the "searchBox" field