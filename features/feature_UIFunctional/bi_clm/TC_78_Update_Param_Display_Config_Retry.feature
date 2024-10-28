@portal @tc78
Feature: Update parameters for portal - Display config: Timeout
  This feature test the functionality related to Display config for Timeout value

  Scenario: Display config for Update paramters: Timeout
    Given I read test data for testcase
    When I click on "refresh" button
    Then "In-progress" response should be appear in the Display config results for the created request 
    Then "Timeout" response should be appear in the Display config results for the created request
