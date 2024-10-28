@TC_56
Feature: RollBack - Execute rollback request: Timeout
  This feature tests the functionality related to execute the rollback request - Timeout

  Scenario: Execute rollback request: Timeout
    Given I read test data for testcase
    When I validate that the "Execute" button should be clickable
    Then I click on "Execute" button
    Then I fill the required parameter for Expected config box
    When I click on "submit" button
    Then Wait for the "errorMessage" popup to appear
    And I validate that the "yesConfirmationRequest" button should be clickable
    When I click on "yesConfirmationRequest" button
    Then "Transactions" page title should be "Transactions"
    When I wait for the "Transactions page" to load
    Then I validate that the created transaction should be in "Submitted" state
    And I wait for the transaction state to be changed to "Timeout"
    And I click on "servicesSidebar" button