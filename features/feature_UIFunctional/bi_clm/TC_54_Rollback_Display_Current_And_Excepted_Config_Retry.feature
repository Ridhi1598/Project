@TC_54
Feature: RollBack - Display current and expected config: Retry
  This feature tests the functionality related to displaying the current and expected config - Retry

  Scenario: Display current and expected config: Retry
    Given I read test data for testcase
    When I click on "retryButton" button
    Then "In-progress" response should be appear in the Display config results for the created request 
    When "Timeout" response should be appear in the Display config results for the created request
    Then I validate that the "Cancel" button should be clickable
    When I click on "Cancel" button
    Then I click on "Confirm" button
    Then I validate the pop-up message for "Cancel request"
    And I click on "servicesSidebar" button