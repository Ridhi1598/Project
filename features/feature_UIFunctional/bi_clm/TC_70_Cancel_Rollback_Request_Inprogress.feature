@TC_70
Feature: Cancel the RollBack request when Request is in in-progress state
  This feature tests the functionality related to Cancel the Rollback request when the request is in in-progress state

  Scenario: Cancel the RollBack request when Request is in in-progress state
    Given I read test data for testcase
#    When I navigate to "services" page
    Then "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    Then I click on "advanceFilter" button
    When I search the service by "CSID" only
    Then I Validate that the Service state should be "active"
    Then I go to "Services" page
    When I click on "rollback" button
    Then I wait for the loader to be disabled
    And I wait for the "parameterInformation" element to be visible
    When I select the version from the dropdown to rollback the service   
    Then I click on "yesConfirmationRequest" button
    When "ServiceUpdate" page title should be "Service Update Queue"
    Then "In-progress" response should be appear in the Display config results for the created request 
    Then I validate that the "Cancel" button should be clickable
    When I click on "Cancel" button
    And I validate that the "Confirm" button should be clickable
    When I click on "Confirm" button
    Then I validate the pop-up message for "Cancel request"
    And I click on "servicesSidebar" button


