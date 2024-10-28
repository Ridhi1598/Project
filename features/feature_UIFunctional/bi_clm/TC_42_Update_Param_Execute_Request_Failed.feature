@portal @tc42
Feature: Update parameters for Execute Request - Failed
  This feature tests the functionality related to update parameters for Execute Request - Failed

  Scenario: Tests the functionality related to update parameters for Execute Request - Failed
    Given I read test data for testcase
    Then I validate that the "Execute" button should be clickable
    When I click on "Execute" button
    Then I fill the required parameter for Expected config box
    When I click on "submit" button
    Then Wait for the "errorMessage" popup to appear
    And I validate that the "yesConfirmationRequest" button should be clickable
    When I click on "yesConfirmationRequest" button
    Then "Transactions" page title should be "Transactions"
    When I wait for the "Transactions page" to load
    Then I validate that the created transaction should be in "Submitted" state
    And Mock "failed" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I wait for the transaction state to be changed to "Failed"
    And I click on "servicesSidebar" button