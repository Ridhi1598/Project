@portal @tc43
Feature: Update parameters for Execute Request - Timeout
  This feature tests the functionality related to update parameters for Execute Request - Timeout

  Scenario: Tests the functionality related to update parameters for Execute Request - Timeout
    Given I read test data for testcase
    When I validate that the "Execute" button should be clickable
    Then I click on "Execute" button
    When I fill the required parameter for Expected config box
    Then I click on "submit" button
    Then Wait for the "errorMessage" popup to appear
    And I validate that the "yesConfirmationRequest" button should be clickable
    When I click on "yesConfirmationRequest" button
    Then "Transactions" page title should be "Transactions"
    When I wait for the "Transactions page" to load
    Then I validate that the created transaction should be in "Submitted" state
    And I wait for the transaction state to be changed to "Timeout"
    And I click on "servicesSidebar" button
